"""
DaBones

Show reader

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.contracts.service import *
from animacy.contracts.performance import *
from animacy.midi.file_reader import MidiFileReader

from animacy.utils.logging import CRITICAL, DEBUG, INFO, log

class ShowReader:
    """Show reader."""

    def __init__(self, next: MidiMessageProcessor, reader: MidiFileReader) -> None:
        """Initialize ShowReader."""
        self.next = next
        self.reader = reader

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        log(1, DEBUG, message.id, message.timecode)
        # Always pass the message along first so the messages we load
        # are not wiped out downstream of us.
        result = PerformanceMessageResult.SKIPPED
        if (isinstance(message, PerformanceLoadSongMessage)):
            log(1706, INFO, message.song)
            self.reader.open(f"{message.song}.mid")
            return PerformanceMessageResult.HANDLED
        return result

    def service(self) -> ServiceResult:
        #  Read files if it's open
        if (self.reader.midi is not None):

            log(1707, CRITICAL)
            handled = 0
            skipped = 0
            for event in self.reader.get_events():
                result = self.next.map(event.timecode, event.message)
                if result == MidiMessageResult.SKIPPED:
                    skipped += 1
                if result == MidiMessageResult.HANDLED:
                    handled += 1

            log(1708, CRITICAL, handled, skipped)
            self.reader.close()
            return ServiceResult.LOADED

        return ServiceResult.IDLE
