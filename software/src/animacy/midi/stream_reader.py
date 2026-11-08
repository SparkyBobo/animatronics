"""
Animacy

Parses (Adafruit) MIDI messages from streams.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.contracts.service import *
from animacy.midi.messages import *
from adafruit_midi.midi_message import MIDIBadEvent, MIDIUnknownEvent
from adafruit_midi.system_exclusive import SystemExclusive
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.midi_continue import Continue
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.active_sensing import ActiveSensing

from animacy.utils.logging import INFO, WARNING, log

class MidiStreamReader(Service):
    """Parses MIDI messages from streams."""

    def __init__(self, next: MidiMessageProcessor = None) -> None:
        """Initialize MidiParser."""
        self.next = next   

    def open(self, device) -> None:
        """Open the selected device."""
        self.device = device

    def close(self) -> None:
        """Close the open file."""
        self.device = None

    def service(self) -> ServiceResult:
        #  Receive MIDI input and retransmit
        msg = self.device.receive()
        return_msg = None
        if msg is None:
            return ServiceResult.IDLE

        # Voice Messages
        elif isinstance(msg, NoteOff):
            log(1223, INFO, msg.channel, msg.note, msg.velocity)
            return_msg = MidiNoteOff(channel=msg.channel, note=msg.note, velocity=msg.velocity)

        elif isinstance(msg, NoteOn):
            log(1224, INFO, msg.channel, msg.note, msg.velocity)
            return_msg = MidiNoteOn(channel=msg.channel, note=msg.note, velocity=msg.velocity)

        elif isinstance(msg, ControlChange):
            log(1225, INFO, msg.channel, msg.control, msg.value)
            if (msg.control == 120):
                return_msg = MidiAllSoundOff(channel=msg.channel)
            elif (msg.control == 123):
                return_msg = MidiAllNotesOff(channel=msg.channel)
            elif (msg.control >= 120):
                return_msg = MidiDeviceMode(channel=msg.channel, control=msg.control, value=msg.value)
            else:
                return_msg = MidiControlChange(channel=msg.channel, control=msg.control, value=msg.value)

        elif isinstance(msg, ProgramChange):
            log(1226, INFO, msg.channel, msg.patch)
            return_msg = MidiProgramChange(channel=msg.channel, program=msg.patch)

        elif isinstance(msg, PitchBend):
            log(1227, INFO, msg.channel, msg.pitch_bend)
            return_msg = MidiPitchBend(channel=msg.channel, bend=msg.pitch_bend)

        # Real time messages
        elif isinstance(msg, TimingClock):
            log(1228, INFO)
            return_msg = MidiClock()

        elif isinstance(msg, Start):
            log(1229, INFO)
            return_msg = MidiSongStart()

        elif isinstance(msg, Stop):
            log(1230, INFO)
            return_msg = MidiSongStop()

        elif isinstance(msg, Continue):
            log(1231, INFO)
            return_msg = MidiSongContinue()

        # elif isinstance(msg, Reset):
        #     logger.info("MIDI Reset")
        #     return_msg = MidiReset()

        elif isinstance(msg, ActiveSensing):
            log(1232, INFO)
            return_msg = MidiActiveSensing()

        elif isinstance(msg, SongSelect):
            log(1233, INFO, msg.id)
            return_msg = MidiSongSelect(song=msg.id)

        elif isinstance(msg, SongPosition):
            log(1234, INFO, msg.position)
            return_msg = MidiSongPosition(position=msg.position)

        elif isinstance(msg, TuneRequest):
            log(1235, INFO)
            return_msg = MidiTuneRequest()

        # System Exclusive
        elif isinstance(msg, SystemExclusive):
            log(1236, INFO, msg.channel)
            usysex_msg = UniversalSystem.from_data_bytes(msg.data, msg.manufacturer_id)
            # Non-Real time
            if (usysex_msg.manufacturer_id == 0x7e):
                if (usysex_msg.subid1 == 0x07 and usysex_msg.subid2 == 0x01):
                    msg = FileHeader.from_sysex_bytes(usysex_msg.channel, usysex_msg.data)
                    return_msg = MidiFileHeader(channel=msg.channel, length=msg.length, name=msg.name)
                elif (usysex_msg.subid1 == 0x07 and usysex_msg.subid2 == 0x02):
                    msg = FileContent.from_sysex_bytes(usysex_msg.channel, usysex_msg.data)
                    return_msg = MidiFileContent(channel=msg.channel, data=msg.data)
                elif (usysex_msg.subid1 == 0x0b and usysex_msg.subid2 == 0x01):
                    msg = FileOpen.from_sysex_bytes(usysex_msg.channel, usysex_msg.data)
                    return_msg = MidiFileOpen(channel=msg.channel, id=msg.id)
                elif (usysex_msg.subid1 == 0x7b):
                    return_msg = MidiFileComplete(channel=msg.channel)
                elif (usysex_msg.subid1 == 0x7d):
                    return_msg = MidiCancel(channel=msg.channel)
                elif (usysex_msg.subid1 == 0x7e):
                    return_msg = MidiNack(channel=msg.channel)
                elif (usysex_msg.subid1 == 0x7f):
                    return_msg = MidiAck(channel=msg.channel)
            # Real time
            elif (usysex_msg.manufacturer_id == 0x7f):
                if (usysex_msg.subid1 == 0x04 and usysex_msg.subid2 == 0x01):
                    msg = VolumeSet.from_data_bytes(usysex_msg.channel, usysex_msg.data)
                    return_msg = MidiVolumeSet(level=msg.level)

        # Unhandled
        elif isinstance(msg, MIDIBadEvent):
            log(1237, WARNING, msg.exception_text, msg.data)
        elif isinstance(msg, MIDIUnknownEvent):
            log(1238, WARNING, msg.status)

        if (return_msg is not None):
            self.next.map(-1, return_msg)            
