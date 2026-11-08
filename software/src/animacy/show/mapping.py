"""
Animacy

Maps MIDI to performance events.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.contracts.performance import *
from animacy.utils.logging import CRITICAL, log


class ShowMapper(MidiMessageProcessor):
    """Maps MIDI to performance events."""

    def __init__(self, next: PerformanceMessageProcessor) -> None:
        """Initialize ShowMapper."""
        self.next = next

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        """Process MidiMessages and pass them to the PerformanceMessageProcessor."""
        perf_msg = None
        if isinstance(
            message,
            (
                MidiNoteOn,
                MidiNoteOff,
                MidiControlChange,
                MidiProgramChange,
                MidiPitchBend,
                MidiDeviceMode,
                MidiAllSoundOff,
                MidiAllNotesOff,
            ),
        ):
            pass

        elif isinstance(message, MidiSongStart):
            perf_msg = PerformanceSongStartMessage(timecode=timecode)

        elif isinstance(message, MidiSongStop):
            perf_msg = PerformanceSongStopMessage(timecode=timecode)

        elif isinstance(message, MidiSongContinue):
            perf_msg = PerformanceSongContinueMessage(timecode=timecode)

        elif isinstance(message, MidiClock):
            perf_msg = PerformanceClockMessage(timecode=timecode)

        elif isinstance(message, MidiFileOpen):
            perf_msg = PerformanceLoadSongMessage(song=message.id, timecode=timecode)

        elif isinstance(message, MidiSongSelect):
            perf_msg = PerformanceLoadSongMessage(song=message.song, timecode=timecode)

        elif isinstance(message, MidiFileHeader):
            perf_msg = PerformanceFileHeaderMessage(name=str(message.name), action="open", timecode=timecode)

        elif isinstance(message, MidiFileContent):
            perf_msg = PerformanceFileContentMessage(data=message.data, timecode=timecode)

        elif isinstance(message, MidiFileComplete):
            perf_msg = PerformanceFileCompleteMessage(checksum=0, timecode=timecode)

        elif isinstance(message, (MidiCancel, MidiNack, MidiAck)):
            pass

        elif isinstance(message, MidiVolumeSet):
            perf_msg = PerformanceVolumeMessage(level=message.level, timecode=timecode)

        elif isinstance(message, MidiSongPosition):
            perf_msg = PerformanceSongPositionMessage(position=message.position, timecode=timecode)

        elif isinstance(message, (MidiTuneRequest, MidiActiveSensing)):
            pass

        elif isinstance(message, MidiReset):
            perf_msg = PerformanceSystemResetMessage(timecode=timecode)

        if (perf_msg is not None):
            log(1704, CRITICAL, type(perf_msg).__name__, perf_msg.timecode)
            self.next.process(perf_msg)
            return MidiMessageResult.HANDLED

        return MidiMessageResult.SKIPPED
