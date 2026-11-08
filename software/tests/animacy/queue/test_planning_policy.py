"""
Animacy

Planning Policy tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import PerformanceControlMessage, PerformanceDataMessage, PerformanceMessageResult
from animacy.queue.planning_policy import PlanningPolicy
from unittest.mock import Mock

def test_policy_init():
    policy = PlanningPolicy(status=Mock())
    assert policy

def test_policy_control():
    status = Mock()
    policy = PlanningPolicy(status)
    message = PerformanceControlMessage()

    status.is_running = False
    status.show_clock = 0
    assert policy.process(message) == PerformanceMessageResult.HANDLED

def test_policy_queue_stopped():
    status = Mock()
    policy = PlanningPolicy(status)
    message = PerformanceDataMessage(timecode=10, events=[])

    status.is_running = False
    status.show_clock = 0
    assert policy.process(message) == PerformanceMessageResult.QUEUED

def test_policy_queue_running():
    status = Mock()
    policy = PlanningPolicy(status)
    message = PerformanceDataMessage(timecode=1050, events=[])

    status.is_running = True
    status.show_clock = 42
    assert policy.process(message) == PerformanceMessageResult.QUEUED

def test_policy_queue_jit():
    status = Mock()
    policy = PlanningPolicy(status)
    message = PerformanceDataMessage(timecode=192+42, events=[])

    status.is_running = True
    status.show_clock = 42
    assert policy.process(message) == PerformanceMessageResult.HANDLED

def test_policy_queue_late():
    status = Mock()
    policy = PlanningPolicy(status)
    message = PerformanceDataMessage(timecode=20, events=[])

    status.is_running = True
    status.show_clock = 42
    assert policy.process(message) == PerformanceMessageResult.SKIPPED

def test_policy_queue_not_too_late():
    status = Mock()
    policy = PlanningPolicy(status)
    message = PerformanceDataMessage(timecode=192+20, events=[])

    status.is_running = True
    status.show_clock = 42
    assert policy.process(message) == PerformanceMessageResult.HANDLED
