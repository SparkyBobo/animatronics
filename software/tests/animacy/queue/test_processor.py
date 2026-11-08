"""
Animacy

Queue processor tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.queue.processor import QueueProcessor
from unittest.mock import Mock

def test_processor_init():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)
    assert processor.next == dispatcher
    assert processor.policy == policy

def test_processor_queue():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.QUEUED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.QUEUED
    assert processor.queue.messages[0] == message

def test_processor_live():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.HANDLED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.HANDLED
    assert not processor.queue.messages

def test_processor_dequeue():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.QUEUED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.QUEUED
    assert processor.queue.messages[0] == message

    policy.process.return_value = PerformanceMessageResult.HANDLED
    clock = PerformanceClockMessage(timecode=100)
    assert processor.process(clock) == PerformanceMessageResult.HANDLED
    assert not processor.queue.messages    
    assert dispatcher.process.call_count == 2

def test_processor_discard():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.QUEUED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.QUEUED
    assert processor.queue.messages[0] == message

    policy.process.return_value = PerformanceMessageResult.HANDLED
    position = PerformanceSongPositionMessage(position=100)
    assert processor.process(position) == PerformanceMessageResult.HANDLED
    assert dispatcher.process.call_count == 1
    assert not processor.queue.messages

def test_processor_system_reset():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.QUEUED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.QUEUED
    assert processor.queue.messages[0] == message

    reset = PerformanceSystemResetMessage()
    assert processor.process(reset) == PerformanceMessageResult.HANDLED
    assert not processor.queue.messages

def test_processor_event_reset():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.QUEUED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.QUEUED
    assert processor.queue.messages[0] == message

    reset = PerformanceResetEventMessage()
    assert processor.process(reset) == PerformanceMessageResult.HANDLED
    assert not processor.queue.messages

def test_processor_load_song():
    dispatcher = Mock()
    policy = Mock()
    processor = QueueProcessor(dispatcher, policy)

    policy.process.return_value = PerformanceMessageResult.QUEUED
    message = PerformanceDataMessage(timecode=10, events=[])
    assert processor.process(message) == PerformanceMessageResult.QUEUED
    assert processor.queue.messages[0] == message

    load_song = PerformanceLoadSongMessage()
    assert processor.process(load_song) == PerformanceMessageResult.HANDLED
    assert not processor.queue.messages


