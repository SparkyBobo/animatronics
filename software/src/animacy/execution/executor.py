"""
Animacy

Executes timed driver transitions.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import DriverTransition
from animacy.contracts.performance import PerformanceMessage, PerformanceMessageResult
from animacy.execution.evaluator import ExecutionEvaluator
from animacy.utils.logging import INFO, log


class Executor:
    """Executes timed driver transitions."""

    def __init__(self, evaluator: ExecutionEvaluator) -> None:
        """Initialize Executor."""
        self.evaluator = evaluator
        self.active_messages = []

    def reset(self) -> None:
        """Reset active transitions."""
        self.active_messages = []

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        """Process events and execute timed driver transitions."""
        if len(message.events):
            if message in self.active_messages:
                return PerformanceMessageResult.HANDLED
            self.active_messages.append(message)
            self.evaluate()
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def evaluate(self) -> PerformanceMessageResult:
        """Process the active messages."""
        read = 0
        write = 0
        length = len(self.active_messages)

        # Read the active list and evaluate each message.
        while read < length:
            active_message = self.active_messages[read]
            read += 1

            # If the evaluator performs and action, compact this item into the list
            (transitions, result) = self.evaluator.evaluate(active_message)
            if transitions:
                log(
                    1401,
                    INFO,
                    len(transitions),
                    active_message.id,
                    active_message.timecode,
                )
                self._dispatch(transitions)

            # If the evaluator performs and action, compact this item into the list
            if result != PerformanceMessageResult.TERMINATE:
                self.active_messages[write] = active_message
                write += 1

        # Delete and items at the end not compacted.
        del self.active_messages[write:]
        log(1402, INFO, len(self.active_messages), write)

    def _dispatch(self, transitions: list[DriverTransition]) -> None:
        """Send transitions to the driver layer."""
        for transition in transitions:
            if transition.driver is not None:
                transition.driver.process(transition)
