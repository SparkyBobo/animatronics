"""
DaBones

Queue tests.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.performance import PerformanceDataMessage
from dabones.queue.queue import PerformanceMessageQueue
from unittest.mock import Mock

def test_processor_init():
    queue = PerformanceMessageQueue()
    assert not queue.messages

def test_processor_queue():
    queue = PerformanceMessageQueue()
    message1 = PerformanceDataMessage(timecode=10, events=[])
    message2 = PerformanceDataMessage(timecode=5, events=[])
    queue.queue(message1)
    queue.queue(message2)
    assert queue.messages[0][2] == message2
    assert queue.messages[1][2] == message1

def test_processor_peek():
    queue = PerformanceMessageQueue()
    message1 = PerformanceDataMessage(timecode=5, events=[])
    message2 = PerformanceDataMessage(timecode=5, events=[])
    message3 = PerformanceDataMessage(timecode=10, events=[])
    queue.queue(message1)
    queue.queue(message2)
    queue.queue(message3)

    peeked_message = queue.peek()
    assert peeked_message == message1
    assert queue.messages[0][2] == message1
    assert queue.messages[1][2] == message2    
    assert queue.messages[2][2] == message3    

def test_processor_dequeue():
    queue = PerformanceMessageQueue()
    message1 = PerformanceDataMessage(timecode=5, events=[])
    message2 = PerformanceDataMessage(timecode=5, events=[])
    message3 = PerformanceDataMessage(timecode=10, events=[])
    queue.queue(message1)
    queue.queue(message2)
    queue.queue(message3)

    dequeued_message = queue.dequeue()
    assert dequeued_message == message1
    assert queue.messages[0][2] == message2
    assert queue.messages[1][2] == message3
