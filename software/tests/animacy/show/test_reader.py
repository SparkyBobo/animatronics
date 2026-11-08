"""
DaBones

Show reader tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

from animacy.contracts.midi import MidiMessageResult
from animacy.contracts.performance import (
    PerformanceClockMessage,
    PerformanceLoadSongMessage,
    PerformanceMessageResult,
)
from animacy.contracts.service import ServiceResult
from animacy.show.reader import ShowReader


def test_reader_opens_requested_song():
    file_reader = Mock()
    show_reader = ShowReader(next=Mock(), reader=file_reader)
    message = PerformanceLoadSongMessage(song="show")

    assert show_reader.process(message) == PerformanceMessageResult.HANDLED

    file_reader.open.assert_called_once_with("show.mid")


def test_reader_skips_non_load_messages():
    file_reader = Mock()
    show_reader = ShowReader(next=Mock(), reader=file_reader)

    assert show_reader.process(PerformanceClockMessage()) == PerformanceMessageResult.SKIPPED
    file_reader.open.assert_not_called()


def test_reader_service_maps_events_then_closes_reader():
    file_reader = Mock()
    file_reader.midi = object()
    file_reader.get_events.return_value = [
        Mock(timecode=4, message="handled"),
        Mock(timecode=8, message="skipped"),
    ]
    mapper = Mock()
    mapper.map.side_effect = [MidiMessageResult.HANDLED, MidiMessageResult.SKIPPED]
    show_reader = ShowReader(next=mapper, reader=file_reader)

    assert show_reader.service() == ServiceResult.LOADED

    assert mapper.map.call_args_list[0].args == (4, "handled")
    assert mapper.map.call_args_list[1].args == (8, "skipped")
    file_reader.close.assert_called_once_with()


def test_reader_service_is_idle_without_open_file():
    file_reader = Mock()
    file_reader.midi = None
    mapper = Mock()
    show_reader = ShowReader(next=mapper, reader=file_reader)

    assert show_reader.service() == ServiceResult.IDLE

    file_reader.get_events.assert_not_called()
    file_reader.close.assert_not_called()
