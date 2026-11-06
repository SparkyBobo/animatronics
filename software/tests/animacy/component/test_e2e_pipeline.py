"""
DaBones

Performance pipeline tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.behavior.eyes import EyesBehavior
from animacy.behavior.rgb import RgbBehavior
from animacy.contracts.performance import *
from animacy.contracts.driver import DriverTransition, AddressableDriverTransition, ColorDriverValue, IntensityDriverValue
from animacy.curves.linear import LinearCurve
from animacy.drivers.led import LedDriver
from animacy.execution.executor import Executor
from animacy.execution.evaluator import ExecutionEvaluator
from animacy.execution.processor import ExecutionProcessor
from animacy.planning.cache import PlanningCache
from animacy.planning.processor import PlanningProcessor
from animacy.queue.planning_policy import PlanningPolicy
from animacy.queue.processor import QueueProcessor
from animacy.queue.show_clock_policy import ShowClockQueuePolicy
from animacy.show.dispatcher import ShowDispatcher
from animacy.show.status import ShowStatusProcessor
from unittest.mock import Mock

def test_e2e_process_queued():

    # Show layer
    show_status = ShowStatusProcessor()

    # Driver layer
    driver = Mock(wraps=LedDriver(count=2))

    # Execution layer
    evaluator = Mock(wraps=ExecutionEvaluator(show_status))
    executor =  Mock(wraps=Executor(evaluator=evaluator))
    execution_processor =  Mock(wraps=ExecutionProcessor(next=None, executor=executor))
    execution_policy = Mock(wraps=ShowClockQueuePolicy(show_status))
    execution_queue = Mock(wraps=QueueProcessor(next=execution_processor, policy=execution_policy))

    # Planning layer
    planner_cache = Mock(wraps=PlanningCache())
    planning_processor = Mock(wraps=PlanningProcessor(next=execution_queue, cache=planner_cache))
    planning_policy = Mock(wraps=PlanningPolicy(show_status))
    planning_queue = Mock(wraps=QueueProcessor(next=planning_processor, policy=planning_policy))

    # Behaviour layer
    left_eye = RgbBehavior(cache=planner_cache, driver=driver, address=1, name="LeftEye")
    right_eye = RgbBehavior(cache=planner_cache, driver=driver, address=2, name="RightEye")
    eyes_behaviour = EyesBehavior(left=left_eye, right=right_eye)
    planning_processor.subscribe(eyes_behaviour)

    # Show layer
    show_processor = Mock(wraps=ShowDispatcher(next=planning_queue, status=show_status))

    # Load the song
    load_message = PerformanceLoadSongMessage(song="Song1")
    show_processor.process(load_message)

    # A song load will start reading a midi file and processing the messages. 
    # For this test, we will simulate a song with a message that change the color and intensity of the eyes.
    eye_message = PerformanceEyeMessage(timecode=5, color=Color(red=255, green=0, blue=0), intensity=128, fade=3)
    show_processor.process(eye_message)

    # At this point, all layers should have received load but eye message was queued, not yet planned.
    assert planning_queue.process.call_count ==  2
    assert planning_processor.process.call_count ==  1
    assert planner_cache.update.call_count == 0
    assert execution_queue.process.call_count == 1
    assert execution_processor.process.call_count ==  1
    assert len(eye_message.events) == 0

    # Start the show clock and schedulers
    start_message = PerformanceSongStartMessage()
    show_processor.process(start_message)

    # At this point, the eye message should have been dequeued and planned, but not yet executed.
    assert planning_queue.process.call_count ==  3
    assert planning_processor.process.call_count ==  3
    assert planner_cache.update.call_count == 4
    assert execution_queue.process.call_count == 3
    assert execution_processor.process.call_count ==  2
    assert len(eye_message.events) == 4
    assert all(isinstance(event.curve, LinearCurve) for event in eye_message.events)    

    # Start the clock
    clock_message = PerformanceClockMessage(timecode=1)
    show_processor.process(clock_message)

    # At this point, the eye message should have been dequeued and planned, but not yet executed.
    assert planning_queue.process.call_count ==  4
    assert planning_processor.process.call_count ==  4
    assert planner_cache.update.call_count == 4
    assert execution_queue.process.call_count == 4
    assert execution_processor.process.call_count ==  3
    assert eye_message.timecode == 2 # message was rescheduled to the earliest event start time
    assert len(eye_message.events) == 4
    assert all(isinstance(event.curve, LinearCurve) for event in eye_message.events)
    assert eye_message.events[0].start == 2
    assert eye_message.events[0].end == 5
    assert eye_message.events[1].start == 2
    assert eye_message.events[1].end == 5
    assert eye_message.events[2].start == 2
    assert eye_message.events[2].end == 5
    assert eye_message.events[3].start == 2
    assert eye_message.events[3].end == 5

    # Advance clock
    clock_message = PerformanceClockMessage(timecode=2)
    show_processor.process(clock_message)

    # At this point, the eye message should have begun execution, and the driver should have received the starting commands.
    assert planning_queue.process.call_count ==  5
    assert planning_processor.process.call_count ==  5
    assert planner_cache.update.call_count == 4
    assert execution_queue.process.call_count == 5
    assert execution_processor.process.call_count ==  5

    # Assert commands were sent to execution
    assert executor.process.call_count ==  1
    assert executor.evaluate.call_count ==  2
    assert len(executor._mock_wraps.active_messages) == 1

    # Assert commands executed by the driver
    assert driver.process.call_count == 4
    first = driver.process.call_args_list[0].args[0]
    second = driver.process.call_args_list[1].args[0]
    third = driver.process.call_args_list[2].args[0]
    fourth = driver.process.call_args_list[3].args[0]
    assert isinstance(first, AddressableDriverTransition)
    assert isinstance(first.start_value, ColorDriverValue)
    assert first.start_value == ColorDriverValue(Color(0, 0, 0))
    assert first.address == 1
    assert first.progress == 0.0
    assert isinstance(second, DriverTransition)
    assert isinstance(second.end_value, IntensityDriverValue)
    assert second.start_value == IntensityDriverValue(0)
    assert second.progress == 0.0
    assert isinstance(third, AddressableDriverTransition)
    assert third.start_value == ColorDriverValue(Color(0, 0, 0))
    assert third.address == 2
    assert third.progress == 0.0
    assert isinstance(fourth, DriverTransition)
    assert fourth.start_value == IntensityDriverValue(0)
    assert fourth.progress == 0.0
    assert all(planner_cache.get(event.transition) == (event.transition.end_value, event.end) for event in eye_message.events)

    # Advance clock
    clock_message = PerformanceClockMessage(timecode=3)
    show_processor.process(clock_message)

    assert executor.process.call_count ==  1
    assert executor.evaluate.call_count ==  3
    assert len(executor._mock_wraps.active_messages) == 1
    assert driver.process.call_count == 8
    assert driver.process.call_args_list[4].args[0].progress == 0.3333333333333333
    assert driver.process.call_args_list[5].args[0].progress == 0.3333333333333333
    assert driver.process.call_args_list[6].args[0].progress == 0.3333333333333333
    assert driver.process.call_args_list[7].args[0].progress == 0.3333333333333333

    # Advance clock
    clock_message = PerformanceClockMessage(timecode=4)
    show_processor.process(clock_message)

    assert executor.process.call_count ==  1
    assert executor.evaluate.call_count ==  4
    assert len(executor._mock_wraps.active_messages) == 1
    assert driver.process.call_count == 12
    assert driver.process.call_args_list[8].args[0].progress == 0.6666666666666666
    assert driver.process.call_args_list[9].args[0].progress == 0.6666666666666666
    assert driver.process.call_args_list[10].args[0].progress == 0.6666666666666666
    assert driver.process.call_args_list[11].args[0].progress == 0.6666666666666666

    # Advance clock
    clock_message = PerformanceClockMessage(timecode=5)
    show_processor.process(clock_message)

    assert executor.process.call_count ==  1
    assert executor.evaluate.call_count ==  5
    assert len(executor._mock_wraps.active_messages) == 0
    assert driver.process.call_count == 16

    # Assert commands executed by the driver
    assert executor.process.call_count ==  1
    assert executor.evaluate.call_count ==  5
    assert len(executor._mock_wraps.active_messages) == 0
    assert driver.process.call_count == 16
    first = driver.process.call_args_list[12].args[0]
    second = driver.process.call_args_list[13].args[0]
    third = driver.process.call_args_list[14].args[0]
    fourth = driver.process.call_args_list[15].args[0]
    assert isinstance(first, AddressableDriverTransition)
    assert isinstance(first.start_value, ColorDriverValue)
    assert first.end_value.color == Color(red=255, green=0, blue=0)
    assert first.address == 1
    assert first.progress == 1.0
    assert isinstance(second, DriverTransition)
    assert isinstance(second.end_value, IntensityDriverValue)
    assert second.end_value.intensity == 128
    assert second.progress == 1.0
    assert isinstance(third, AddressableDriverTransition)
    assert third.end_value.color == Color(red=255, green=0, blue=0)
    assert third.address == 2
    assert third.progress == 1.0
    assert isinstance(fourth, DriverTransition)
    assert fourth.end_value.intensity == 128
    assert fourth.progress == 1.0
    assert all(planner_cache.get(event.transition) == (event.transition.end_value, event.end) for event in eye_message.events)


