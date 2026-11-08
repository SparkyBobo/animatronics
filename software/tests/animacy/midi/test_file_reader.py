"""
Animacy

MIDI file reader tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.midi.file_reader import MidiFileReader
import mido
import logging

def test_reader_init():
    reader = MidiFileReader()
    assert reader
    assert not reader.file_info
    assert not reader.track_info

def test_reader_file_info():
    test_file = "test.mid"
    mid = get_test_file()
    mid.save(test_file)

    reader = MidiFileReader()
    reader.open(test_file)

    assert reader.file_info
    assert reader.file_info.sequence == 42
    assert reader.file_info.name == 'Show42'
    assert reader.file_info.tempo == 250000
    assert reader.file_info.miditicks_per_quarter == 480

def test_reader_show_1():
    reader = MidiFileReader()
    reader.open("1.mid")

    assert reader.midi.miditicks_per_quarter == 960
    assert len(reader.midi.tracks) == 7

    logger = logging.getLogger(__name__)

    count = 0
    for event in reader.get_events():
        count += 1

    assert count == 3925


def test_reader_show_2():
    reader = MidiFileReader()
    reader.open("2.mid")

    assert reader.midi.miditicks_per_quarter == 960
    assert len(reader.midi.tracks) == 7

    count = 0
    for event in reader.get_events():
        count += 1

    assert count == 2885


def test_reader_track_info_1():
    test_file = "test.mid"
    mid = get_test_file()
    mid.save(test_file)

    reader = MidiFileReader()
    reader.open(test_file)
    reader.select_track(1)

    assert reader.track_info
    assert reader.track_info.name == 'Joey'
    assert reader.track_info.channel == 1

    expected = [
        MidiTrackEvent(timecode=1, message=MidiNoteOff(channel=1, note=60, velocity=0)),
        MidiTrackEvent(timecode=2, message=MidiNoteOn(channel=1, note=61, velocity=40)),
        MidiTrackEvent(timecode=3, message=MidiControlChange(channel=1, control=1, value=40)),
        MidiTrackEvent(timecode=4, message=MidiProgramChange(channel=1, program=62)),
        MidiTrackEvent(timecode=5, message=MidiPitchBend(channel=1, bend=100)),
    ]

    events = list(reader.get_events())
    assert [event.message for event in events] == [
        event.message for event in expected
    ]
    assert [event.timecode for event in events] == [0, 0, 0, 0, 1]

    for event in events:
        assert isinstance(event, MidiTrackEvent)


def test_reader_track_info_2():
    test_file = "test.mid"
    mid = get_test_file()
    mid.save(test_file)

    reader = MidiFileReader()
    reader.open(test_file)
    reader.select_track(2)

    assert reader.track_info
    assert reader.track_info.name == 'Slash'
    assert reader.track_info.channel == 2

    expected = [
        MidiTrackEvent(timecode=1, message=MidiNoteOff(channel=2, note=70, velocity=0)),
        MidiTrackEvent(timecode=2, message=MidiNoteOn(channel=2, note=71, velocity=127)),
        MidiTrackEvent(timecode=3, message=MidiControlChange(channel=2, control=2, value=42)),
        MidiTrackEvent(timecode=4, message=MidiProgramChange(channel=2, program=72)),
        MidiTrackEvent(timecode=5, message=MidiPitchBend(channel=2, bend=1000)),
    ]

    events = list(reader.get_events())
    assert [event.message for event in events] == [
        event.message for event in expected
    ]
    assert [event.timecode for event in events] == [0, 0, 0, 0, 1]

    for event in events:
        assert isinstance(event, MidiTrackEvent)

def test_reader_missing_track_clears_selection(tmp_path):
    reader = MidiFileReader()
    assert reader.select_track(1) is None

    filename = tmp_path / "test.mid"
    get_test_file().save(filename)
    reader.open(str(filename))
    reader.select_track(1)

    assert reader.select_track(99) is None
    assert reader.track_info is None

def test_reader_maps_all_sound_off_and_all_notes_off_and_skips_unknown_controls(tmp_path):
    midi_file = get_test_file()
    track = midi_file.tracks[1]
    track.pop()
    track.extend([
        mido.Message("control_change", channel=1, control=120, value=0, time=1),
        mido.Message("control_change", channel=1, control=123, value=0, time=1),
        mido.Message("control_change", channel=1, control=121, value=0, time=1),
        mido.MetaMessage("end_of_track"),
    ])
    filename = tmp_path / "controls.mid"
    midi_file.save(filename)

    reader = MidiFileReader()
    reader.open(str(filename))
    assert reader.select_track(1) is not None
    events = list(reader.get_events())

    assert [event.message for event in events[-2:]] == [
        MidiAllSoundOff(channel=1),
        MidiAllNotesOff(channel=1),
    ]
    assert len(events) == 7

def get_test_file():
    meta_track = mido.MidiTrack()
    meta_track.append(mido.MetaMessage('sequence_number', number=42, time=0))
    meta_track.append(mido.MetaMessage('track_name', name='Show42', time=0))
    meta_track.append(mido.MetaMessage('instrument_name', name='meta', time=0))
    meta_track.append(mido.MetaMessage('channel_prefix', channel=0, time=0))
    meta_track.append(mido.MetaMessage('set_tempo', tempo=250000, time=0))
    meta_track.append(mido.MetaMessage('end_of_track'))
    ch1_track = mido.MidiTrack()
    ch1_track.append(mido.MetaMessage('instrument_name', name='Joey', time=0))
    ch1_track.append(mido.MetaMessage('channel_prefix', channel=1, time=0))
    ch1_track.append(mido.Message('note_off', channel=1, note=60, velocity=0, time=1))
    ch1_track.append(mido.Message('note_on', channel=1, note=61, velocity=40, time=2))
    ch1_track.append(mido.Message('control_change', channel=1, control=1, value=40, time=3))
    ch1_track.append(mido.Message('program_change', channel=1, program=62, time=4))
    ch1_track.append(mido.Message('pitchwheel', channel=1, pitch=100, time=5))
    ch1_track.append(mido.MetaMessage('end_of_track'))
    ch2_track = mido.MidiTrack()
    ch2_track.append(mido.MetaMessage('instrument_name', name='Slash', time=0))
    ch2_track.append(mido.MetaMessage('channel_prefix', channel=2, time=0))
    ch2_track.append(mido.Message('note_off', channel=2, note=70, velocity=0, time=1))
    ch2_track.append(mido.Message('note_on', channel=2, note=71, velocity=127, time=2))
    ch2_track.append(mido.Message('control_change', channel=2, control=2, value=42, time=3))
    ch2_track.append(mido.Message('program_change', channel=2, program=72, time=4))
    ch2_track.append(mido.Message('pitchwheel', channel=2, pitch=1000, time=5))
    ch2_track.append(mido.MetaMessage('end_of_track'))
    mid = mido.MidiFile(type=1, ticks_per_beat=480)
    mid.tracks.append(meta_track)
    mid.tracks.append(ch1_track)
    mid.tracks.append(ch2_track)
    return mid
