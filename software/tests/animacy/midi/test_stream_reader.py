"""
Animacy

Stream reader tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

import pytest
from adafruit_midi.active_sensing import ActiveSensing
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_continue import Continue
from adafruit_midi.midi_message import MIDIBadEvent, MIDIUnknownEvent
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.system_exclusive import SystemExclusive
from adafruit_midi.timing_clock import TimingClock

from animacy.midi.messages import (
    FileContent,
    FileHeader,
    FileOpen,
    SongPosition,
    SongSelect,
    TuneRequest,
    UniversalSystem,
    VolumeSet,
)
from animacy.contracts.midi import (
    MidiActiveSensing,
    MidiAck,
    MidiAllNotesOff,
    MidiAllSoundOff,
    MidiClock,
    MidiControlChange,
    MidiFileComplete,
    MidiFileContent,
    MidiFileHeader,
    MidiFileOpen,
    MidiDeviceMode,
    MidiCancel,
    MidiNack,
    MidiNoteOff,
    MidiNoteOn,
    MidiPitchBend,
    MidiProgramChange,
    MidiSongContinue,
    MidiSongPosition,
    MidiSongSelect,
    MidiSongStart,
    MidiSongStop,
    MidiTuneRequest,
    MidiVolumeSet,
)
from animacy.contracts.service import ServiceResult
from animacy.midi.stream_reader import MidiStreamReader


@pytest.mark.parametrize(
    ("raw_message", "expected"),
    [
        (NoteOff(channel=2, note=64, velocity=7), MidiNoteOff(channel=2, note=64, velocity=7)),
        (NoteOn(channel=3, note=65, velocity=96), MidiNoteOn(channel=3, note=65, velocity=96)),
        (
            ControlChange(channel=4, control=1, value=2),
            MidiControlChange(channel=4, control=1, value=2),
        ),
        (
            ControlChange(channel=4, control=120, value=0),
            MidiAllSoundOff(channel=4),
        ),
        (
            ControlChange(channel=4, control=123, value=0),
            MidiAllNotesOff(channel=4),
        ),
        (
            ControlChange(channel=4, control=124, value=1),
            MidiDeviceMode(channel=4, control=124, value=1),
        ),
        (ProgramChange(channel=5, patch=9), MidiProgramChange(channel=5, program=9)),
        (PitchBend(channel=6, pitch_bend=1000), MidiPitchBend(channel=6, bend=1000)),
        (TimingClock(), MidiClock()),
        (Start(), MidiSongStart()),
        (Stop(), MidiSongStop()),
        (Continue(), MidiSongContinue()),
        (ActiveSensing(), MidiActiveSensing()),
        (SongSelect(7), MidiSongSelect(song=7)),
        (SongPosition(321), MidiSongPosition(position=321)),
        (TuneRequest(), MidiTuneRequest()),
    ],
)
def test_stream_reader_maps_adafruit_messages(raw_message, expected):
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    reader.open(Mock(receive=Mock(return_value=raw_message)))

    assert reader.service() == ServiceResult.ACTIVITY

    downstream.map.assert_called_once_with(-1, expected)


def test_stream_reader_is_idle_when_no_message_is_available():
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    reader.open(Mock(receive=Mock(return_value=None)))

    assert reader.service() == ServiceResult.IDLE
    downstream.map.assert_not_called()


def test_stream_reader_ignores_unknown_message():
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    reader.open(Mock(receive=Mock(return_value=MIDIUnknownEvent(0xF5))))

    assert reader.service() == ServiceResult.ACTIVITY

    downstream.map.assert_not_called()


def test_stream_reader_ignores_unrecognized_system_exclusive_message():
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    reader.open(
        Mock(
            receive=Mock(
                return_value=SystemExclusive(manufacturer_id=b"\x01", data=b"\x00")
            )
        )
    )

    assert reader.service() == ServiceResult.ACTIVITY
    downstream.map.assert_not_called()


@pytest.mark.parametrize(
    "raw_message",
    [
        UniversalSystem(channel=1, sub1=0x01, sub2=0, data=b""),
        UniversalSystem(channel=1, sub1=0x05, sub2=0, data=b""),
        UniversalSystem(channel=1, sub1=0x04, sub2=0x02, data=b"", manufacturer_id=0x7f),
    ],
)
def test_stream_reader_ignores_unrecognized_universal_message(raw_message):
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    manufacturer_id, channel, sub1, sub2 = (
        raw_message.manufacturer_id,
        raw_message.channel,
        raw_message.sub1,
        raw_message.sub2,
    )
    payload = getattr(raw_message, "encoded_data", raw_message.data)
    sysex = SystemExclusive(
        manufacturer_id=bytes([manufacturer_id]),
        data=bytes([channel, sub1, sub2]) + payload,
    )
    reader.open(Mock(receive=Mock(return_value=sysex)))

    assert reader.service() == ServiceResult.ACTIVITY
    downstream.map.assert_not_called()


def test_stream_reader_ignores_malformed_and_unknown_events():
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    device = Mock()
    device.receive.side_effect = [
        MIDIBadEvent(bytearray([0x90]), ValueError("incomplete")),
        MIDIUnknownEvent(0xF5),
    ]
    reader.open(device)

    assert reader.service() == ServiceResult.ACTIVITY
    assert reader.service() == ServiceResult.ACTIVITY
    downstream.map.assert_not_called()


@pytest.mark.parametrize(
    ("raw_message", "expected"),
    [
        (
            FileHeader(channel=2, length=200, name="show.mid"),
            MidiFileHeader(channel=2, length=200, name="show.mid"),
        ),
        (
            FileContent(channel=3, data=b"\x00\x80\xff"),
            MidiFileContent(channel=3, data=b"\x00\x80\xff"),
        ),
        (
            FileOpen(channel=4, id=321),
            MidiFileOpen(channel=4, id=321),
        ),
        (
            UniversalSystem(channel=5, sub1=0x7b, sub2=0, data=b""),
            MidiFileComplete(channel=5),
        ),
        (
            UniversalSystem(channel=6, sub1=0x7d, sub2=0, data=b""),
            MidiCancel(channel=6),
        ),
        (
            UniversalSystem(channel=7, sub1=0x7e, sub2=0, data=b""),
            MidiNack(channel=7),
        ),
        (
            UniversalSystem(channel=8, sub1=0x7f, sub2=0, data=b""),
            MidiAck(channel=8),
        ),
        (
            VolumeSet(channel=9, level=300),
            MidiVolumeSet(channel=9, level=300),
        ),
    ],
)
def test_stream_reader_maps_universal_system_exclusive_messages(raw_message, expected):
    downstream = Mock()
    reader = MidiStreamReader(next=downstream)
    manufacturer_id, channel, sub1, sub2 = (
        raw_message.manufacturer_id,
        raw_message.channel,
        raw_message.sub1,
        raw_message.sub2,
    )
    payload = getattr(raw_message, "encoded_data", raw_message.data)
    sysex = SystemExclusive(
        manufacturer_id=bytes([manufacturer_id]),
        data=bytes([channel, sub1, sub2]) + payload,
    )
    reader.open(Mock(receive=Mock(return_value=sysex)))

    assert reader.service() == ServiceResult.ACTIVITY

    downstream.map.assert_called_once_with(-1, expected)


def test_stream_reader_close_clears_device():
    reader = MidiStreamReader()
    reader.open(Mock())

    reader.close()

    assert reader.device is None
