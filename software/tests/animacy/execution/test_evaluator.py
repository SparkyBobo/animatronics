"""
Animacy

Execution evaluator tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

from animacy.contracts.performance import (
    PerformanceDataMessage,
    PerformanceEvent,
    PerformanceMessageResult,
)
from animacy.execution.evaluator import ExecutionEvaluator
from animacy.show.status import ShowStatusProcessor


def test_evaluator_init():
    evaluator = ExecutionEvaluator(status=ShowStatusProcessor())
    assert evaluator is not None


def test_executor_terminated():
    evaluator = ExecutionEvaluator(status=ShowStatusProcessor())

    transition1 = Mock()
    transition2 = Mock()
    message = PerformanceDataMessage(
        timecode=10,
        events=[
            PerformanceEvent(transition=transition1, start=-1, end=0),
            PerformanceEvent(transition=transition2, start=-1, end=0),
        ],
    )
    (transitions, result) = evaluator.evaluate(message)

    assert transitions == [transition1, transition2]
    assert result == PerformanceMessageResult.TERMINATE


def test_evaluator_skips_events_without_transitions():
    evaluator = ExecutionEvaluator(status=ShowStatusProcessor())
    message = PerformanceDataMessage(
        events=[PerformanceEvent(transition=None), PerformanceEvent(transition=None)]
    )

    transitions, result = evaluator.evaluate(message)

    assert transitions == []
    assert result == PerformanceMessageResult.TERMINATE
