"""
DaBones

Executes timed driver transitions.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import DriverTransition, DriverValue
from animacy.contracts.performance import *
from animacy.execution.evaluator import ExecutionEvaluator

import logging
logger = logging.getLogger(__name__)

class Executor:
    """Executes timed driver transitions."""

    def __init__(self, evaluator: ExecutionEvaluator) -> None:
        """Initialize Executor."""
        self.evaluator = evaluator
        self.active_messages = []
        pass

    def reset(self) -> None:
        """Reset active transitions."""
        self.active_messages = []

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        """Process events and execute timed driver transitions."""
        if (len(message.events)):
            self.active_messages.append(message)
            self.evaluate()

    def evaluate(self) -> PerformanceMessageResult:
        """Process the active messages."""
        read = 0
        write = 0
        length = len(self.active_messages)

        # Read the active list and evaluate each message.
        while (read < length):
            active_message = self.active_messages[read]
            read += 1

            # If the evaluator performs and action, compact this item into the list
            (transitions, result) = self.evaluator.evaluate(active_message)
            if transitions:
                logger.info(f"Dispatch {len(transitions)} transitions for performance message {active_message.id}@{active_message.timecode}")
                self._dispatch(transitions)

            # If the evaluator performs and action, compact this item into the list
            if (result != PerformanceMessageResult.TERMINATE):
                self.active_messages[write] = active_message
                write += 1

        # Delete and items at the end not compacted.
        del self.active_messages[write:]
        logger.info(f"Trim active messages to {len(self.active_messages)}@{write}")

    def _dispatch(self, transitions: list[DriverTransition]) -> None:
        """Send transitions to the driver layer."""
        for transition in transitions:
            if (transition.driver is not None):
                transition.driver.process(transition)
