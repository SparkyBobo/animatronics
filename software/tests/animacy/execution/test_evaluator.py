
"""
Animacy

Executor tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.execution.evaluator import ExecutionEvaluator
from animacy.show.status import ShowStatusProcessor
from unittest.mock import Mock

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