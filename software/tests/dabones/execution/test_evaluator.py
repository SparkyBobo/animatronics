
"""
DaBones

Executor tests.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.performance import *
from dabones.execution.evaluator import ExecutionEvaluator
from dabones.show.status import ShowStatus
from unittest.mock import Mock

def test_evaluator_init():
    evaluator = ExecutionEvaluator(status=ShowStatus())
    assert evaluator is not None

def test_executor_terminated():
    evaluator = ExecutionEvaluator(status=ShowStatus())

    transition1 = Mock()
    transition2 = Mock()
    message = PerformanceDataMessage(
        timecode=10,
        events=[
            PerformanceEvent(transition=transition1),
            PerformanceEvent(transition=transition2),
        ],
    )
    (transitions, result) = evaluator.evaluate(message)

    assert transitions == [transition1, transition2]
    assert result == PerformanceMessageResult.TERMINATE