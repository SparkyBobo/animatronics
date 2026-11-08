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
