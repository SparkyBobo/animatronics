"""
Animacy

Show reader

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import MidiMessageProcessor, MidiMessageResult
from animacy.contracts.performance import (
    PerformanceLoadSongMessage,
    PerformanceMessage,
    PerformanceMessageResult,
)
from animacy.contracts.service import ServiceResult
from animacy.midi.file_reader import MidiFileReader
from animacy.utils.logging import CRITICAL, DEBUG, INFO, CatalogLogger
from animacy.utils.memory import (
    AFTER_MIDI_LOAD,
    AFTER_SHOW_READER_INIT,
    BEFORE_MIDI_LOAD,
    MemoryMonitor,
)

logger = CatalogLogger(__name__)
memory = MemoryMonitor()


class ShowReader:
    """Show reader."""

    def __init__(self, next: MidiMessageProcessor, reader: MidiFileReader) -> None:
        """Initialize ShowReader."""
        self.next = next
        self.reader = reader
        memory.record(AFTER_SHOW_READER_INIT)

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        logger.log(1, DEBUG, message.id, message.timecode)
        # Always pass the message along first so the messages we load
        # are not wiped out downstream of us.
        result = PerformanceMessageResult.SKIPPED
        if isinstance(message, PerformanceLoadSongMessage):
            logger.log(1706, INFO, message.song)
            memory.record(BEFORE_MIDI_LOAD)
            self.reader.open(f"{message.song}.mid")
            memory.record(AFTER_MIDI_LOAD)
            return PerformanceMessageResult.HANDLED
        return result

    def service(self) -> ServiceResult:
        #  Read files if it's open
        if self.reader.midi is not None:
            logger.log(1707, CRITICAL)
            handled = 0
            skipped = 0
            for event in self.reader.get_events():
                result = self.next.map(event.timecode, event.message)
                if result == MidiMessageResult.SKIPPED:
                    skipped += 1
                if result == MidiMessageResult.HANDLED:
                    handled += 1

            logger.log(1708, CRITICAL, handled, skipped)
            self.reader.close()
            return ServiceResult.LOADED

        return ServiceResult.IDLE
