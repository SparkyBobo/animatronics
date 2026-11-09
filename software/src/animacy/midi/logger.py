"""
Animacy

Logs messages.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import(
    MidiAck,
    MidiActiveSensing,
    MidiCancel,
    MidiClock,
    MidiControlChange,
    MidiFileComplete,
    MidiFileContent,
    MidiFileHeader,
    MidiFileOpen,
    MidiMessage,
    MidiMessageResult,
    MidiNack,
    MidiNoteOff,
    MidiNoteOn,
    MidiPitchBend,
    MidiProgramChange,
    MidiReset,
    MidiSongContinue,
    MidiSongPosition,
    MidiSongSelect,
    MidiSongStart,
    MidiSongStop,
    MidiTuneRequest,
    MidiVolumeSet,
)
from animacy.utils.logging import INFO, CatalogLogger

logger = CatalogLogger(__name__)

class MidiMessageLogger:
    """Logs the midi messages."""

    def __init__(self) -> None:
        """Initialize MidiMessageDispatcher."""
        pass

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
            if isinstance(message, MidiNoteOn):
                logger.log(1201, INFO, message.channel, message.note, message.velocity, timecode)

            elif isinstance(message, MidiNoteOff):
                logger.log(1202, INFO, message.channel, message.note, message.velocity, timecode)

            elif isinstance(message, MidiControlChange):
                logger.log(1203, INFO, message.channel, message.control, message.value, timecode)
                # class MidiDeviceMode(MidiControlChange):
                # class MidiAllSoundOff(MidiChannelMessage):
                # class MidiAllNotesOff(MidiChannelMessage):

            elif isinstance(message, MidiProgramChange):
                logger.log(1204, INFO, message.channel, message.program, timecode)

            elif isinstance(message, MidiPitchBend):
                logger.log(1205, INFO, message.channel, message.bend, timecode)

            elif isinstance(message, MidiSongStart):
                logger.log(1206, INFO, timecode)

            elif isinstance(message, MidiSongStop):
                logger.log(1207, INFO, timecode)

            elif isinstance(message, MidiSongContinue):
                logger.log(1208, INFO, timecode)

            elif isinstance(message, MidiClock):
                logger.log(1209, INFO, timecode)

            elif isinstance(message, MidiFileHeader):
                logger.log(1210, INFO, message.name, message.length, timecode)

            elif isinstance(message, MidiFileContent):
                logger.log(1211, INFO, len(message.data), timecode)

            elif isinstance(message, MidiFileComplete):
                logger.log(1212, INFO, timecode)

            elif isinstance(message, MidiFileOpen):
                logger.log(1213, INFO, message.id, timecode)

            elif isinstance(message, MidiCancel):
                logger.log(1214, INFO, timecode)

            elif isinstance(message, MidiNack):
                logger.log(1215, INFO, timecode)

            elif isinstance(message, MidiAck):
                logger.log(1216, INFO, timecode)

            elif isinstance(message, MidiVolumeSet):
                logger.log(1217, INFO, message.level, timecode)

            elif isinstance(message, MidiSongSelect):
                logger.log(1218, INFO, message.song, timecode)

            elif isinstance(message, MidiSongPosition):
                logger.log(1219, INFO, message.position, timecode)

            elif isinstance(message, MidiTuneRequest):
                logger.log(1220, INFO, timecode)

            elif isinstance(message, MidiActiveSensing):
                logger.log(1221, INFO, timecode)

            elif isinstance(message, MidiReset):
                logger.log(1222, INFO, timecode)
