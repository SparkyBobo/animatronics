"""
DaBones

Performance message contract tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.color import Color
from animacy.contracts.performance import (
    PerformanceBendNoteMessage,
    PerformanceEyeMessage,
    PerformanceNeckPositionMessage,
    PerformancePercussionStrikeMessage,
    PerformancePlayNoteMessage,
    PerformancePlayTechiqueMessage,
    PerformanceRythmicMotionMessage,
    PerformanceSingMessage,
)


def test_data_message_constructors_preserve_values_and_initialize_events():
    messages = [
        (
            1,
            PerformancePlayNoteMessage(timecode=1, note=60, intensity=80),
            {"note": 60, "intensity": 80},
        ),
        (
            2,
            PerformancePlayTechiqueMessage(timecode=2, technique=3, intensity=81),
            {"technique": 3, "intensity": 81},
        ),
        (
            3,
            PerformanceBendNoteMessage(timecode=3, bend=12, intensity=82),
            {"bend": 12, "intensity": 82},
        ),
        (
            4,
            PerformancePercussionStrikeMessage(
                timecode=4, target="snare", intensity=83
            ),
            {"target": "snare", "intensity": 83},
        ),
        (5, PerformanceSingMessage(timecode=5, intensity=84), {"intensity": 84}),
        (
            6,
            PerformanceNeckPositionMessage(timecode=6, position=25, intensity=85),
            {"position": 25, "intensity": 85},
        ),
        (
            7,
            PerformanceRythmicMotionMessage(timecode=7, frequency=2, intensity=86),
            {"frequency": 2, "intensity": 86},
        ),
        (
            8,
            PerformanceEyeMessage(
                timecode=8, color=Color(1, 2, 3, 4), intensity=87, fade=9
            ),
            {"color": Color(1, 2, 3, 4), "intensity": 87, "fade": 9},
        ),
    ]

    for timecode, message, expected_attributes in messages:
        assert message.timecode == timecode
        assert message.events == []
        for name, value in expected_attributes.items():
            assert getattr(message, name) == value
