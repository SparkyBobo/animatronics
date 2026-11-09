"""
Animacy

Execution executor tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

from animacy.contracts.performance import (
    PerformanceDataMessage,
    PerformanceEvent,
    PerformanceMessageResult,
)
from animacy.execution.executor import Executor


def _message():
    return PerformanceDataMessage(events=[PerformanceEvent()])


def _transition(driver):
    transition = Mock()
    transition.driver = driver
    return transition


def test_executor_init():
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)
    assert executor.evaluator == evaluator
    assert executor.active_messages == []


def test_executor_handled():
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)

    driver = Mock()
    command1 = _transition(driver)
    command2 = _transition(driver)
    evaluator.evaluate.return_value = (
        [command1, command2],
        PerformanceMessageResult.HANDLED,
    )

    message = _message()
    executor.process(message)
    assert executor.active_messages == [message]
    assert driver.process.call_count == 2
    driver.process.assert_any_call(command1)
    driver.process.assert_any_call(command2)


def test_executor_evaluates_again_at_same_clock():
    evaluator = Mock()
    evaluator.status.show_clock = 0
    driver = Mock()
    transition = _transition(driver)
    evaluator.evaluate.return_value = ([transition], PerformanceMessageResult.HANDLED)
    executor = Executor(evaluator=evaluator)

    executor.process(_message())
    executor.evaluate()

    assert evaluator.evaluate.call_count == 2
    assert driver.process.call_count == 2


def test_executor_does_not_activate_the_same_message_twice():
    evaluator = Mock()
    evaluator.evaluate.return_value = ([], PerformanceMessageResult.HANDLED)
    executor = Executor(evaluator=evaluator)
    message = _message()

    executor.process(message)
    executor.process(message)

    assert executor.active_messages == [message]
    evaluator.evaluate.assert_called_once_with(message)


def test_executor_terminated():
    driver = Mock()
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)

    command1 = _transition(driver)
    command2 = _transition(driver)
    evaluator.evaluate.return_value = (
        [command1, command2],
        PerformanceMessageResult.TERMINATE,
    )

    message = _message()
    executor.process(message)
    assert executor.active_messages == []
    assert driver.process.call_count == 2
    driver.process.assert_any_call(command1)
    driver.process.assert_any_call(command2)


def test_executor_compressed():
    driver = Mock()
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)

    command1 = _transition(driver)
    command2 = _transition(driver)
    evaluator.evaluate.side_effect = [
        # executor.process(message1)
        ([command1, command2], PerformanceMessageResult.HANDLED),
        # executor.process(message2)
        ([command1, command2], PerformanceMessageResult.HANDLED),
        ([command1, command2], PerformanceMessageResult.HANDLED),
        # executor.process(message3)
        ([command1, command2], PerformanceMessageResult.HANDLED),
        ([command1, command2], PerformanceMessageResult.TERMINATE),
        ([command1, command2], PerformanceMessageResult.HANDLED),
    ]

    message1 = _message()
    message2 = _message()
    message3 = _message()
    executor.process(message1)
    executor.process(message2)
    executor.process(message3)
    assert executor.active_messages == [message1, message3]
    assert driver.process.call_count == 12  # 2 transitions across 6 evaluations
