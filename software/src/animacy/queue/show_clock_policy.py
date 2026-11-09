"""
Animacy

Policy to release items based on the show clock.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import (
    PerformanceControlMessage,
    PerformanceMessage,
    PerformanceMessageResult,
)
from animacy.contracts.show import ShowStatus
from animacy.utils.logging import INFO, CatalogLogger

logger = CatalogLogger(__name__)


class ShowClockQueuePolicy:
    """Queues and dequeues messages against the show clock."""

    def __init__(self, status: ShowStatus) -> None:
        """Initialize message queue."""
        logger.log(5, INFO)
        self.status = status

    def _get_clock(self) -> int:
        """Get the current show clock."""
        return self.status.show_clock

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        logger.log(2, INFO, message.id, message.timecode)
        if isinstance(message, PerformanceControlMessage):
            return PerformanceMessageResult.HANDLED
        elif not self.status.is_running:
            return PerformanceMessageResult.QUEUED

        show_clock = self._get_clock()
        if message.timecode == show_clock:
            return PerformanceMessageResult.HANDLED
        elif message.timecode < show_clock:
            return PerformanceMessageResult.SKIPPED
        else:
            return PerformanceMessageResult.QUEUED
