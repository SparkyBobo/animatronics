"""
DaBones

Logs messages.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.utils.logging import INFO, log

class MidiMessageLogger:
    """Logs the midi messages."""

    def __init__(self) -> None:
        """Initialize MidiMessageDispatcher."""
        pass

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
            if isinstance(message, MidiNoteOn):
                log(1201, INFO, message.channel, message.note, message.velocity, timecode)

            elif isinstance(message, MidiNoteOff):
                log(1202, INFO, message.channel, message.note, message.velocity, timecode)

            elif isinstance(message, MidiControlChange):
                log(1203, INFO, message.channel, message.control, message.value, timecode)
                # class MidiDeviceMode(MidiControlChange):
                # class MidiAllSoundOff(MidiChannelMessage):
                # class MidiAllNotesOff(MidiChannelMessage):

            elif isinstance(message, MidiProgramChange):
                log(1204, INFO, message.channel, message.program, timecode)

            elif isinstance(message, MidiPitchBend):
                log(1205, INFO, message.channel, message.bend, timecode)

            elif isinstance(message, MidiSongStart):
                log(1206, INFO, timecode)

            elif isinstance(message, MidiSongStop):
                log(1207, INFO, timecode)

            elif isinstance(message, MidiSongContinue):
                log(1208, INFO, timecode)

            elif isinstance(message, MidiClock):
                log(1209, INFO, timecode)

            elif isinstance(message, MidiFileHeader):
                log(1210, INFO, message.name, message.length, timecode)

            elif isinstance(message, MidiFileContent):
                log(1211, INFO, len(message.data), timecode)

            elif isinstance(message, MidiFileComplete):
                log(1212, INFO, timecode)

            elif isinstance(message, MidiFileOpen):
                log(1213, INFO, message.id, timecode)

            elif isinstance(message, MidiCancel):
                log(1214, INFO, timecode)

            elif isinstance(message, MidiNack):
                log(1215, INFO, timecode)

            elif isinstance(message, MidiAck):
                log(1216, INFO, timecode)

            elif isinstance(message, MidiVolumeSet):
                log(1217, INFO, message.level, timecode)

            elif isinstance(message, MidiSongSelect):
                log(1218, INFO, message.song, timecode)

            elif isinstance(message, MidiSongPosition):
                log(1219, INFO, message.position, timecode)

            elif isinstance(message, MidiTuneRequest):
                log(1220, INFO, timecode)

            elif isinstance(message, MidiActiveSensing):
                log(1221, INFO, timecode)

            elif isinstance(message, MidiReset):
                log(1222, INFO, timecode)
