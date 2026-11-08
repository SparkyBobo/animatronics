"""
Animacy

Policy to release items based on the show clock.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.show import ShowStatus
from animacy.contracts.performance import PerformanceMessage, PerformanceControlMessage, PerformanceMessageResult
from animacy.queue.show_clock_policy import ShowClockQueuePolicy

from animacy.utils.logging import INFO, log

class PlanningPolicy(ShowClockQueuePolicy):
    """Queues and dequeues messages against the show clock."""

    def __init__(self, status: ShowStatus) -> None:
        """Initialize message queue."""
        log(5, INFO)
        self.status = status

    def _get_clock(self) -> int:
        """Get the current show clock."""
        # We cheat here, let planning run a bit ahead of
        # the show clock to allow for planning of events
        show_clock = self.status.show_clock
        return show_clock + 192

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        log(2, INFO, message.id, message.timecode)
        # Since we're running ahead, make sure not to skip messages that are just a bit late
        if (self.status.is_running and message.timecode > self.status.show_clock):
            if (message.timecode < self._get_clock()):
                return PerformanceMessageResult.HANDLED
        return super().process(message)
