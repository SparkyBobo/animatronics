"""
DaBones

Show file manager

Copyright (c) 2026 Sparky Bobo
"""

from animacy.show.reader import ShowReader
from animacy.contracts.performance import PerformanceMessage, PerformanceMessageResult

import logging
logger = logging.getLogger(__name__)

class ShowFileManager:
    """Show file managers."""

    def __init__(self, reader: ShowReader) -> None:
        """Initialize ShowClock."""
        self.reader = reader
        pass

    def process(self, event:PerformanceMessage) -> PerformanceMessageResult:
        pass
