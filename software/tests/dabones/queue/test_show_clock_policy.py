"""
DaBones

Show Clock Policy tests.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.performance import PerformanceControlMessage, PerformanceDataMessage, PerformanceMessageResult
from dabones.queue.show_clock_policy import ShowClockQueuePolicy
from unittest.mock import Mock

def test_policy_init():
    policy = ShowClockQueuePolicy(status=Mock())
    assert policy

def test_policy_control():
    status = Mock()
    policy = ShowClockQueuePolicy(status)
    message = PerformanceControlMessage()

    status.is_running = False
    status.show_clock = 0
    assert policy.process(message) == PerformanceMessageResult.HANDLED

def test_policy_queue_stopped():
    status = Mock()
    policy = ShowClockQueuePolicy(status)
    message = PerformanceDataMessage(timecode=10, events=[])

    status.is_running = False
    status.show_clock = 0
    assert policy.process(message) == PerformanceMessageResult.QUEUED

def test_policy_queue_running():
    status = Mock()
    policy = ShowClockQueuePolicy(status)
    message = PerformanceDataMessage(timecode=50, events=[])

    status.is_running = True
    status.show_clock = 4
    assert policy.process(message) == PerformanceMessageResult.QUEUED

def test_policy_queue_jit():
    status = Mock()
    policy = ShowClockQueuePolicy(status)
    message = PerformanceDataMessage(timecode=42, events=[])

    status.is_running = True
    status.show_clock = 42
    assert policy.process(message) == PerformanceMessageResult.HANDLED

def test_policy_queue_late():
    status = Mock()
    policy = ShowClockQueuePolicy(status)
    message = PerformanceDataMessage(timecode=20, events=[])

    status.is_running = True
    status.show_clock = 42
    assert policy.process(message) == PerformanceMessageResult.SKIPPED
