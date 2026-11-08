"""
Animacy

Execution processor tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.execution.processor import ExecutionProcessor
from unittest.mock import Mock

def test_processor_init():
    dispatcher = Mock()
    executor = Mock()
    processor = ExecutionProcessor(dispatcher, executor)
    assert processor.next == dispatcher
    assert processor.executor == executor

def test_processor_execute():
    dispatcher = Mock()
    executor = Mock()
    processor = ExecutionProcessor(dispatcher, executor)

    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.SKIPPED
    executor.process.assert_called_once_with(message)
    dispatcher.process.assert_called_once_with(message)

def test_processor_resets_executor_for_song_position():
    dispatcher = Mock()
    executor = Mock()
    processor = ExecutionProcessor(dispatcher, executor)
    message = PerformanceSongPositionMessage(position=42)

    assert processor.process(message) == PerformanceMessageResult.HANDLED

    executor.reset.assert_called_once_with()
    executor.process.assert_called_once_with(message)
    dispatcher.process.assert_called_once_with(message)

def test_processor_evaluates_executor_on_clock():
    dispatcher = Mock()
    executor = Mock()
    processor = ExecutionProcessor(dispatcher, executor)
    message = PerformanceClockMessage(timecode=42)

    assert processor.process(message) == PerformanceMessageResult.HANDLED

    executor.evaluate.assert_called_once_with()
    executor.process.assert_called_once_with(message)
    dispatcher.process.assert_called_once_with(message)

def test_processor_stops_propagation_when_executor_terminates():
    dispatcher = Mock()
    executor = Mock()
    executor.process.return_value = PerformanceMessageResult.TERMINATE
    processor = ExecutionProcessor(dispatcher, executor)
    message = PerformanceDataMessage()

    assert processor.process(message) == PerformanceMessageResult.TERMINATE

    dispatcher.process.assert_not_called()
