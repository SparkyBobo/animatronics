"""
DaBones

MIDI-to-performance mapping tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

import pytest

from animacy.contracts.midi import (
    MidiAck,
    MidiActiveSensing,
    MidiAllNotesOff,
    MidiAllSoundOff,
    MidiCancel,
    MidiClock,
    MidiControlChange,
    MidiDeviceMode,
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
from animacy.contracts.performance import (
    PerformanceClockMessage,
    PerformanceFileCompleteMessage,
    PerformanceFileContentMessage,
    PerformanceFileHeaderMessage,
    PerformanceLoadSongMessage,
    PerformanceSongContinueMessage,
    PerformanceSongPositionMessage,
    PerformanceSongStartMessage,
    PerformanceSongStopMessage,
    PerformanceSystemResetMessage,
    PerformanceVolumeMessage,
)
from animacy.show.mapping import ShowMapper


@pytest.mark.parametrize(
    ("midi_message", "expected_type", "attributes"),
    [
        (MidiSongStart(), PerformanceSongStartMessage, {}),
        (MidiSongStop(), PerformanceSongStopMessage, {}),
        (MidiSongContinue(), PerformanceSongContinueMessage, {}),
        (MidiClock(), PerformanceClockMessage, {}),
        (MidiFileOpen(id="song"), PerformanceLoadSongMessage, {"song": "song"}),
        (MidiSongSelect(song="song"), PerformanceLoadSongMessage, {"song": "song"}),
        (
            MidiFileHeader(name="show.mid"),
            PerformanceFileHeaderMessage,
            {"name": "show.mid", "action": "open"},
        ),
        (
            MidiFileContent(data=b"midi"),
            PerformanceFileContentMessage,
            {"data": b"midi"},
        ),
        (MidiFileComplete(), PerformanceFileCompleteMessage, {"checksum": 0}),
        (MidiVolumeSet(level=73), PerformanceVolumeMessage, {"level": 73}),
        (
            MidiSongPosition(position=321),
            PerformanceSongPositionMessage,
            {"position": 321},
        ),
        (MidiReset(), PerformanceSystemResetMessage, {}),
    ],
)
def test_mapper_translates_supported_messages(midi_message, expected_type, attributes):
    downstream = Mock()
    mapper = ShowMapper(next=downstream)

    assert mapper.map(42, midi_message) == MidiMessageResult.HANDLED

    downstream.process.assert_called_once()
    performance_message = downstream.process.call_args.args[0]
    assert isinstance(performance_message, expected_type)
    assert performance_message.timecode == 42
    for name, value in attributes.items():
        assert getattr(performance_message, name) == value


@pytest.mark.parametrize(
    "midi_message",
    [
        MidiNoteOn(channel=1, note=60, velocity=100),
        MidiNoteOff(channel=1, note=60, velocity=0),
        MidiControlChange(channel=1, control=1, value=2),
        MidiProgramChange(channel=1, program=3),
        MidiPitchBend(channel=1, bend=4),
        MidiDeviceMode(),
        MidiAllSoundOff(),
        MidiAllNotesOff(),
        MidiCancel(),
        MidiNack(),
        MidiAck(),
        MidiTuneRequest(),
        MidiActiveSensing(),
        MidiMessage(),
    ],
)
def test_mapper_skips_unmapped_messages(midi_message):
    downstream = Mock()
    mapper = ShowMapper(next=downstream)

    assert mapper.map(42, midi_message) == MidiMessageResult.SKIPPED
    downstream.process.assert_not_called()
