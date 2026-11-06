"""
DaBones

Show runner

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *

import logging
logger = logging.getLogger(__name__)

class ShowRunner:
    """Show runner."""

    def __init__(self) -> None:
        """Initialize ShowRunner."""
        pass

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceSongStartMessage):
            logger.info(f"Process song start message {message.id}@{message.timecode}")

        elif isinstance(message, PerformanceSongStopMessage):
            logger.info(f"Process song stop message {message.id}@{message.timecode}")

        elif isinstance(message, PerformanceSongContinueMessage):
            logger.info(f"Process song continue message {message.id}@{message.timecode}")
