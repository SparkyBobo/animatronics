"""
DaBones

Audio behavior tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

import pytest

from animacy.behavior.audio import AudioBehavior
from animacy.contracts.driver import AudioDriverValue
from animacy.contracts.performance import (
    PerformanceClockMessage,
    PerformanceLoadSongMessage,
    PerformanceMessageResult,
    PerformanceResetEventMessage,
    PerformanceSongContinueMessage,
    PerformanceSongPositionMessage,
    PerformanceSongStartMessage,
    PerformanceSongStopMessage,
    PerformanceVolumeMessage,
)


@pytest.mark.parametrize(
    ("message", "expected_result", "expected_command"),
    [
        (
            PerformanceResetEventMessage(timecode=4),
            PerformanceMessageResult.HANDLED,
            "STOP",
        ),
        (
            PerformanceLoadSongMessage(timecode=5, song="song"),
            PerformanceMessageResult.HANDLED,
            "LOAD song.wav",
        ),
        (
            PerformanceSongStartMessage(timecode=6),
            PerformanceMessageResult.HANDLED,
            "START",
        ),
        (
            PerformanceSongStopMessage(timecode=7),
            PerformanceMessageResult.HANDLED,
            "STOP",
        ),
        (PerformanceSongContinueMessage(), PerformanceMessageResult.SKIPPED, None),
        (PerformanceSongPositionMessage(), PerformanceMessageResult.SKIPPED, None),
        (PerformanceVolumeMessage(), PerformanceMessageResult.SKIPPED, None),
        (PerformanceClockMessage(), PerformanceMessageResult.SKIPPED, None),
    ],
)
def test_audio_behavior_processes_playback_commands(
    message, expected_result, expected_command
):
    behavior = AudioBehavior(driver=Mock(), name="audio")

    result = behavior.process(message)

    assert result == expected_result
    if expected_command is None:
        assert message.events == []
    else:
        assert len(message.events) == 1
        event = message.events[0]
        assert event.start == message.timecode
        assert event.end == message.timecode
        assert event.transition.end_value == AudioDriverValue(expected_command)


def test_audio_behavior_midi_mapping_is_skipped():
    assert AudioBehavior(driver=Mock(), name="audio").map(0, Mock()) == 0
