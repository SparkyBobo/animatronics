"""
DaBones

That status of the show.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.contracts.show import ShowStatus
import time

import logging
logger = logging.getLogger(__name__)

class ShowStatusProcessor:
    """Tracks the state of the show."""

    def __init__(self) -> None:
        """Initialize show status."""
        logger.info("Initialize ShowStatus.")
        self._reset()

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        logger.info(f"Process performance message {message.id}@{message.timecode}")
        if (isinstance(message, PerformanceSystemResetMessage) or isinstance(message, PerformanceResetEventMessage)):
            self._reset()
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceLoadSongMessage)):
            self._pause()
            self._update(0)
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongPositionMessage)):
            self._pause()
            self._update(message.position)
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongStopMessage)):
            self._pause()
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongStartMessage)):
            self._play()
            self._update(0)
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongContinueMessage)):
            self._play()
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceClockMessage)):
            if (self.show_clock == 0):
                self.start_clock = time.monotonic()
                self.next_clock_tick = time.monotonic()
            self._update(self.show_clock+1 if message.timecode is -1 else message.timecode)
            message.timecode = self.show_clock
            return PerformanceMessageResult.HANDLED

        return PerformanceMessageResult.SKIPPED

    def _reset(self) -> None:
        """Reset the show status."""
        self.is_running = False
        self.show_clock = 0
        self.start_clock = 0
        self.next_clock_tick = 0

    def _pause(self) -> None:
        """Pause the show status."""
        logger.info("Pause ShowStatus.")
        self.is_running = False
        self.next_clock_tick = time.monotonic()

    def _play(self) -> None:
        """Play the show status."""
        logger.info("Play ShowStatus.")
        self.is_running = True
        self.next_clock_tick = time.monotonic()

    def _update(self, show_clock: int) -> None:
        """Update the show clock. """
        self.show_clock = show_clock