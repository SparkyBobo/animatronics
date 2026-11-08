"""
Animacy

Evaluated performance messages for execution.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.show import ShowStatus
from animacy.contracts.driver import DriverTransition
from animacy.contracts.performance import *

import logging
logger = logging.getLogger(__name__)

class ExecutionEvaluator:
    """Extracts driver transitions from performance events."""

    def __init__(self, status: ShowStatus) -> None:
        """Initialize ExecutionEvaluator."""
        #logger.info("Initialize ExecutionEvaluator.")
        self.status = status

    def evaluate(self, message: PerformanceDataMessage) -> tuple[list[tuple[DriverTransition]], PerformanceMessageResult]:
        """Evaluate events and extract their driver transitions."""
        #logger.info(f"Evaluate performance message {message.id}@{message.timecode}")
        transitions = []
        result = PerformanceMessageResult.TERMINATE
        for event in message.events or []:
            if event.transition is not None:
                # This transition has priority.
                if (event.end == -1):
                    event.transition.progress = 1.0
                    transitions.append(event.transition)

                # This transition is ending/ended.
                if (event.end <= self.status.show_clock):
                    event.transition.progress = 1.0
                    if (event.end == self.status.show_clock):
                        transitions.append(event.transition)

                # This transition is starting.
                elif (event.start <= self.status.show_clock):
                    event.transition.progress = 0.0
                    transitions.append(event.transition)
                    result = PerformanceMessageResult.HANDLED

                # This transition is active if the show clock is between the start and end time of the event.
                elif (event.start < self.status.show_clock and event.end > self.status.show_clock):
                    event.transition.progress = event.curve.progress(event.start, event.end, self.status.show_clock)
                    transitions.append(event.transition)
                    result = PerformanceMessageResult.HANDLED

                # This transition is pending.
                elif (event.start < self.status.show_clock):
                    result = PerformanceMessageResult.SKIPPED

        #logger.info(f"Evaluated performance message with {len(message.events)}: {len(transitions)} transitions, result={result}")
        return (transitions, result)
