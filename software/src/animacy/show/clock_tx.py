"""
Animacy

Transmits performance clock.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *

import logging
logger = logging.getLogger(__name__)

class PerformanceClockTransmitter:
    """Transmits performance clock."""

    def __init__(self) -> None:
        """Initialize PerformanceClockTransmitter."""
        pass

    def process(self, msg:PerformanceMessage) -> PerformanceMessageResult:
        """Process performance messages to start/stop clock."""
        pass
        #PerformanceShowInformation
        #PerformanceSystemResetMessage
        #PerformanceLoadSongMessage
        #PerformanceSongStartMessage
        #PerformanceSongContinueMessage
        #PerformanceSongStopMessage
        #PerformanceSongPositionMessage

