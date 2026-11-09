"""
Animacy

Evaluated performance messages for execution.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.contracts.driver import DriverTransition
from animacy.contracts.performance import (
    PerformanceDataMessage,
    PerformanceMessageResult,
)
from animacy.contracts.show import ShowStatus

logger = logging.getLogger(__name__)


class ExecutionEvaluator:
    """Extracts driver transitions from performance events."""

    def __init__(self, status: ShowStatus) -> None:
        """Initialize ExecutionEvaluator."""
        # logger.info("Initialize ExecutionEvaluator.")
        self.status = status

    def evaluate(
        self, message: PerformanceDataMessage
    ) -> tuple[list[tuple[DriverTransition]], PerformanceMessageResult]:
        """Evaluate events and extract their driver transitions."""
        # logger.info(f"Evaluate performance message {message.id}@{message.timecode}")
        transitions = []
        result = PerformanceMessageResult.TERMINATE
        for event in message.events or []:
            if event.transition is None:
                continue

            show_clock = self.status.show_clock
            if event.end == -1:
                event.transition.progress = 1.0
                transitions.append(event.transition)
                result = PerformanceMessageResult.HANDLED
            elif show_clock < event.start:
                result = PerformanceMessageResult.HANDLED
            elif show_clock >= event.end:
                if show_clock == event.end:
                    event.transition.progress = 1.0
                    transitions.append(event.transition)
            else:
                event.transition.progress = event.curve.progress(
                    event.start,
                    event.end,
                    show_clock,
                )
                transitions.append(event.transition)
                result = PerformanceMessageResult.HANDLED

        # logger.info(f"Evaluated performance message with {len(message.events)}: {len(transitions)} transitions, result={result}")
        return (transitions, result)
