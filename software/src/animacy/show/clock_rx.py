"""
Animacy

Receives performance clock.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *

import logging
logger = logging.getLogger(__name__)

class PerformanceClockReceiver:
    """Receives performance clock."""

    def __init__(self, processor: PerformanceMessageProcessor) -> None:
        """Initialize PerformanceClockReceiver."""
        self.processor = processor

    def process(self, msg:PerformanceMessage) -> PerformanceMessageResult:
        """Process performance messages to start/stop clock."""
        pass
        #PerformanceSystemResetMessage
        #PerformanceLoadSongMessage
        #PerformanceSongStartMessage
        #PerformanceSongContinueMessage
        #PerformanceSongStopMessage
        #PerformanceSongPositionMessage        

    def _dispatch(self, timecode: int) -> None:
        """Dispatch the received timecode."""
        message = PerformanceClockMessage(timecode=timecode)
        self.processor.process(message)


