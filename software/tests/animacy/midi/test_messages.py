"""
DaBones

Custom MIDI message tests.

Copyright (c) 2026 Sparky Bobo
"""

import pytest

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


@pytest.mark.parametrize(
    ("message", "expected_bytes"),
    [
        (SongSelect(12), bytes([0xF1, 12])),
        (SongPosition(321), bytes([0xF2, 65, 2])),
        (TuneRequest(), bytes([0xF6])),
    ],
)
def test_system_common_messages_round_trip(message, expected_bytes):
    assert bytes(message) == expected_bytes

    decoded = type(message).from_bytes(expected_bytes)

    assert bytes(decoded) == expected_bytes


def test_universal_system_encodes_and_decodes_payload():
    message = UniversalSystem(channel=3, sub1=7, sub2=1, data=b"payload")

    decoded = UniversalSystem.from_data_bytes(
        bytes([message.channel, message.sub1, message.sub2]) + message.data,
        message.manufacturer_id,
    )

    assert decoded.channel == 3
    assert decoded.sub1 == 7
    assert decoded.sub2 == 1
    assert decoded.data == b"payload"
    assert bytes(decoded) == bytes(message)


def test_universal_system_accepts_full_sysex_and_raw_data_forms():
    message = UniversalSystem(channel=3, sub1=7, sub2=1, data=b"payload")

    assert bytes(UniversalSystem.from_bytes(bytes(message))) == bytes(message)
    assert bytes(
        UniversalSystem.from_sysex_bytes(
            bytes([message.channel, message.sub1, message.sub2]) + message.data
        )
    ) == bytes(message)
    assert UniversalSystem.from_data_bytes(
        bytes([message.channel, message.sub1, message.sub2]) + message.data,
        b"\x7e",
    ).manufacturer_id == 0x7e


def test_universal_system_rejects_short_data():
    with pytest.raises(ValueError, match="must contain channel and sub-identifiers"):
        UniversalSystem.from_data_bytes(b"\x01", 0x7e)


def test_file_header_encodes_and_decodes_name_and_length():
    message = FileHeader(channel=2, length=123456, name="show.mid")

    decoded = FileHeader.from_sysex_bytes(message.channel, message.data)

    assert decoded.length == 123456
    assert decoded.name == "show.mid"
    assert bytes(decoded) == bytes(message)


def test_file_header_rejects_invalid_payload():
    with pytest.raises(ValueError, match="Invalid MIDI file header"):
        FileHeader.from_sysex_bytes(1, b"not-midi")


@pytest.mark.parametrize(
    "payload",
    [b"", b"\x00\x7f\x80\xff", bytes(range(20))],
)
def test_file_content_round_trip_does_not_mutate_input(payload):
    original = payload
    message = FileContent(channel=1, data=payload)

    decoded = FileContent.from_sysex_bytes(message.channel, message.encoded_data)

    assert payload == original
    assert decoded.data == original
    assert bytes(decoded) == bytes(message)


@pytest.mark.parametrize("file_id", [0, 1, 127, 128, 16383])
def test_file_open_round_trip(file_id):
    message = FileOpen(channel=5, id=file_id)

    decoded = FileOpen.from_sysex_bytes(message.channel, message.data)

    assert decoded.id == file_id
    assert bytes(decoded) == bytes(message)


@pytest.mark.parametrize("level", [0, 1, 127, 128, 16383])
def test_volume_set_round_trip(level):
    message = VolumeSet(channel=4, level=level)

    decoded = VolumeSet.from_data_bytes(message.channel, message.data)

    assert decoded.level == level
    assert bytes(decoded) == bytes(message)
