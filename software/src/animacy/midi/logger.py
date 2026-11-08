"""
DaBones

Logs messages.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *

import logging
logger = logging.getLogger(__name__)

class MidiMessageLogger:
    """Logs the midi messages."""

    def __init__(self) -> None:
        """Initialize MidiMessageDispatcher."""
        pass

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
            if isinstance(message, MidiNoteOn):
                logger.info(f"MIDI NoteOn {message.channel}:{message.note}:{message.velocity}@{timecode}")

            elif isinstance(message, MidiNoteOff):
                logger.info(f"MIDI NoteOff {message.channel}:{message.note}:{message.velocity}@{timecode}")

            elif isinstance(message, MidiControlChange):
                logger.info(f"MIDI ControlChange {message.channel}:{message.control}:{message.value}@{timecode})")
                # class MidiDeviceMode(MidiControlChange):
                # class MidiAllSoundOff(MidiChannelMessage):
                # class MidiAllNotesOff(MidiChannelMessage):

            elif isinstance(message, MidiProgramChange):
                logger.info(f"MIDI ProgramChange {message.channel}:{message.program}@{timecode}")

            elif isinstance(message, MidiPitchBend):
                logger.info(f"MIDI PitchBend {message.channel}:{message.bend}@{timecode}")

            elif isinstance(message, MidiSongStart):
                logger.info(f"MIDI Start@{timecode}")

            elif isinstance(message, MidiSongStop):
                logger.info(f"MIDI Stop@{timecode}")

            elif isinstance(message, MidiSongContinue):
                logger.info(f"MIDI Continue@{timecode}")

            elif isinstance(message, MidiClock):
                logger.info(f"MIDI Clock@{timecode}")

            elif isinstance(message, MidiFileHeader):
                logger.info(f"MIDI File Header {message.name}@{message.length}@{timecode}")

            elif isinstance(message, MidiFileContent):
                logger.info(f"MIDI File Content {len(message.data)}@{timecode}")

            elif isinstance(message, MidiFileComplete):
                logger.info(f"MIDI File Complete@{timecode}")

            elif isinstance(message, MidiFileOpen):
                logger.info(f"MIDI File Open {message.id}@{timecode}")

            elif isinstance(message, MidiCancel):
                logger.info(f"MIDI Cancel@{timecode}")

            elif isinstance(message, MidiNack):
                logger.info(f"MIDI Nack@{timecode}")

            elif isinstance(message, MidiAck):
                logger.info(f"MIDI Ack@{timecode}")

            elif isinstance(message, MidiVolumeSet):
                logger.info(f"MIDI Volume {message.level}@{timecode}")

            elif isinstance(message, MidiSongSelect):
                logger.info(f"MIDI Song Select {message.song}@{timecode}")

            elif isinstance(message, MidiSongPosition):
                logger.info(f"MIDI Song Position {message.position}@{timecode}")

            elif isinstance(message, MidiTuneRequest):
                logger.info(f"MIDI Tune Request@{timecode}")

            elif isinstance(message, MidiActiveSensing):
                logger.info(f"MIDI Sensing@{timecode}")

            elif isinstance(message, MidiReset):
                logger.info(f"MIDI Reset@{timecode}")
