"""
Animacy

Show runner

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *

from animacy.utils.logging import INFO, log

class ShowRunner:
    """Show runner."""

    def __init__(self) -> None:
        """Initialize ShowRunner."""
        pass

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceSongStartMessage):
            log(3, INFO, message.id, message.timecode)

        elif isinstance(message, PerformanceSongStopMessage):
            log(4, INFO, message.id, message.timecode)

        elif isinstance(message, PerformanceSongContinueMessage):
            log(1711, INFO, message.id, message.timecode)
