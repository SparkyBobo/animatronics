"""
DaBones

MIDI message logger tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import patch

import pytest

from animacy.contracts.midi import (
    MidiAck,
    MidiActiveSensing,
    MidiCancel,
    MidiClock,
    MidiControlChange,
    MidiFileComplete,
    MidiFileContent,
    MidiFileHeader,
    MidiFileOpen,
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
from animacy.midi.logger import MidiMessageLogger
import animacy.midi.logger as midi_logger_module
from animacy.utils.logging import INFO


@pytest.mark.parametrize(
    ("message", "code", "args"),
    [
        (MidiNoteOn(1, 60, 100), 1201, (1, 60, 100, 25)),
        (MidiNoteOff(1, 60, 0), 1202, (1, 60, 0, 25)),
        (MidiProgramChange(1, 3), 1204, (1, 3, 25)),
        (MidiPitchBend(1, 2048), 1205, (1, 2048, 25)),
        (MidiControlChange(1, 7, 100), 1203, (1, 7, 100, 25)),
        (MidiSongStart(), 1206, (25,)),
        (MidiSongStop(), 1207, (25,)),
        (MidiSongContinue(), 1208, (25,)),
        (MidiClock(), 1209, (25,)),
        (MidiFileHeader(name="song.mid", length=512), 1210, ("song.mid", 512, 25)),
        (MidiFileContent(data=b"data"), 1211, (4, 25)),
        (MidiFileComplete(), 1212, (25,)),
        (MidiFileOpen(id=3), 1213, (3, 25)),
        (MidiCancel(), 1214, (25,)),
        (MidiNack(), 1215, (25,)),
        (MidiAck(), 1216, (25,)),
        (MidiVolumeSet(level=64), 1217, (64, 25)),
        (MidiSongSelect(song=2), 1218, (2, 25)),
        (MidiSongPosition(position=321), 1219, (321, 25)),
        (MidiTuneRequest(), 1220, (25,)),
        (MidiActiveSensing(), 1221, (25,)),
        (MidiReset(), 1222, (25,)),
    ],
)
def test_logger_logs_supported_messages(message, code, args):
    with patch.object(midi_logger_module.logger, "log") as log:
        MidiMessageLogger().map(25, message)

    log.assert_called_once_with(code, INFO, *args)


def test_logger_ignores_unrecognized_message():
    with patch.object(midi_logger_module.logger, "log") as log:
        MidiMessageLogger().map(25, object())

    log.assert_not_called()
