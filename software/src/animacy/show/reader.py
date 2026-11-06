"""
DaBones

Show reader

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.contracts.service import *
from animacy.contracts.performance import *
from animacy.midi.file_reader import MidiFileReader

import logging
logger = logging.getLogger(__name__)

class ShowReader:
    """Show reader."""

    def __init__(self, next: MidiMessageProcessor, reader: MidiFileReader) -> None:
        """Initialize ShowReader."""
        self.next = next
        self.reader = reader

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        logger.debug(f"Process performance message {message.id}@{message.timecode}")
        # Always pass the message along first so the messages we load
        # are not wiped out downstream of us.
        result = PerformanceMessageResult.SKIPPED
        if (isinstance(message, PerformanceLoadSongMessage)):
            logger.info(f"Loading song {message.song}")
            self.reader.open(f"{message.song}.mid")
            return PerformanceMessageResult.HANDLED
        return result

    def service(self) -> ServiceResult:
        #  Read files if it's open
        if (self.reader.midi is not None):

            logger.critical(f"Loading song...")
            handled = 0
            skipped = 0
            for event in self.reader.get_events():
                result = self.next.map(event.timecode, event.message)
                if result == MidiMessageResult.SKIPPED:
                    skipped += 1
                if result == MidiMessageResult.HANDLED:
                    handled += 1

            logger.critical(f"Loaded song with {handled} handled events, {skipped} skipped events")
            self.reader.close()
            return ServiceResult.LOADED

        return ServiceResult.IDLE
