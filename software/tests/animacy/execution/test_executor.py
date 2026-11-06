
"""
DaBones

Executor tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.execution.executor import Executor
from unittest.mock import Mock

def test_executor_init():
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)
    assert executor.evaluator == evaluator
    assert executor.active_messages == []

def test_executor_handled():
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)

    driver = Mock()
    command1 = Mock()
    command2 = Mock()
    evaluator.evaluate.return_value = ([command1, command2], PerformanceMessageResult.HANDLED)

    message = PerformanceDataMessage()
    executor.process(message)
    assert executor.active_messages == [message]
    assert driver.process.call_count == 2
    driver.process.assert_any_call(command1)
    driver.process.assert_any_call(command2)

def test_executor_terminated():
    driver = Mock()
    evaluator = Mock()
    executor = Executor(evaluator=evaluator)

    command1 = Mock()
    command2 = Mock()
    evaluator.evaluate.return_value = ([command1, command2], PerformanceMessageResult.TERMINATE)

    message = PerformanceDataMessage()
    executor.process(message)
    assert executor.active_messages == []
    assert driver.process.call_count == 2
    driver.process.assert_any_call(command1)
    driver.process.assert_any_call(command2)

def test_executor_compressed():
    driver = Mock()
    evaluator = Mock()
    executor = Executor(driver=driver, evaluator=evaluator)

    command1 = Mock()
    command2 = Mock()
    evaluator.evaluate.side_effect = [
        # executor.process(message1)
        ([command1, command2], PerformanceMessageResult.HANDLED),
        # executor.process(message2)
        ([command1, command2], PerformanceMessageResult.HANDLED),
        ([command1, command2], PerformanceMessageResult.TERMINATE),
        # executor.process(message3)
        ([command1, command2], PerformanceMessageResult.HANDLED),
        ([command1, command2], PerformanceMessageResult.HANDLED)
    ]

    message1 = PerformanceDataMessage()
    message2 = PerformanceDataMessage()
    message3 = PerformanceDataMessage()
    executor.process(message1)
    executor.process(message2)
    executor.process(message3)
    assert executor.active_messages == [message1, message3]
    assert driver.process.call_count == 10 # 2 commands * 5 calls



