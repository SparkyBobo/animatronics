"""
DaBones

Reads Standard MIDI Files.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from umidiparser import umidiparser, MidiFile, MidiEvent
import gc

import logging
logger = logging.getLogger(__name__)

class MidiFileReader:
    """Reads Standard MIDI Files."""

    def __init__(self) -> None:
        """Initialize MidiFileReader."""
        self.midi = None
        self._file_info = None
        self.selected_track_info = None
        self.selected_track = None
        pass

    def open(self, filename:str) -> None:
        """Open the selected file."""
        self.midi = umidiparser.MidiFile(filename)
        #self._file_info = self._get_file_info()
        #self.selected_track = None
        #self.selected_track_info = None

    def close(self) -> None:
        """Close the open file."""
        self.midi = None
        self._file_info = None
        self.selected_track = None
        self.selected_track_info = None

    @property
    def file_info(self):
        """
        Return the midi file info.
        """
        return self._file_info

    @property
    def track_info(self):
        """
        Return the selected midi track info.
        """
        return self.selected_track_info

    def select_track(self, channel:int) -> MidiTrackInfo: 
        """
        Returns the MIDI track info for the selected track.
        """
        if (not self.midi):
            return None

        for track in self.midi.tracks:
            track_name = ''
            track_channel = -1
            for event in track:
                if event.status == umidiparser.INSTRUMENT_NAME:
                    track_name = event.name
                elif event.status == umidiparser.CHANNEL_PREFIX:
                    track_channel = event.channel

            if (channel == track_channel):
                self.selected_track = track
                self.selected_track_info = MidiTrackInfo(name=track_name, channel=track_channel)
                return self.selected_track_info

        return None

    def get_events(self):
        track_msg = None
        absolute_ticks = 0
        for event in self.midi:
            absolute_ticks += event.delta_miditicks
            #logger.info(f"Midi read pre-map event freemem={gc.mem_free()}, alloc={gc.mem_alloc()}")


            if event.status == umidiparser.NOTE_OFF:
                track_msg = MidiNoteOff(channel = event.channel, note = event.note, velocity = event.velocity)
            elif event.status == umidiparser.NOTE_ON:
                track_msg = MidiNoteOn(channel = event.channel, note = event.note, velocity = event.velocity)
            elif event.status == umidiparser.CONTROL_CHANGE:
                if (event.control < 120):
                    track_msg = MidiControlChange(channel = event.channel, control = event.control, value = event.value)
                if (event.control == 120):
                    track_msg = MidiAllSoundOff(channel = event.channel)
                if (event.control == 123):
                    track_msg = MidiAllNotesOff(channel = event.channel)
            elif event.status == umidiparser.PROGRAM_CHANGE:
                track_msg = MidiProgramChange(channel = event.channel, program = event.program)
            elif event.status == umidiparser.PITCHWHEEL:
                track_msg = MidiPitchBend(channel = event.channel, bend = event.pitch)
            else:
                continue # skip        

            # At 120 bpm and 960 PPQN and 24 MIDI Clock pulses per quarter note, 
            # the conversion is exactly 40 file ticks per MIDI Clock pulse.
            timecode = round(absolute_ticks/40)
            yield MidiTrackEvent(timecode=timecode, message=track_msg)
            

    def _get_file_info(self) -> MidiFileInfo: 
        """
        Returns the MIDI track for the metadata track, channel 0.
        """
        for track in self.midi.tracks:
            channel_prefix = -1
            file_sequence = -1
            file_name = ''
            file_tempo = -1
            file_ppqn = -1
            for event in track:
                if event.status == umidiparser.CHANNEL_PREFIX:
                    channel_prefix = event.channel
                elif event.status == umidiparser.SEQUENCE_NUMBER:
                    file_sequence = event.number
                elif event.status == umidiparser.TRACK_NAME:
                    file_name = event.name
                elif event.status == umidiparser.SET_TEMPO:
                    file_tempo = event.tempo

            if (channel_prefix == 0):
                return MidiFileInfo(sequence=file_sequence, name=file_name, tempo=file_tempo, miditicks_per_quarter=self.midi.miditicks_per_quarter)

        return None    


