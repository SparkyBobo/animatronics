"""
DaBones

Stream reader tests.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.midi import *
from dabones.midi.stream_reader import MidiStreamReader
import mido

def test_reader_init():
    reader = MidiStreamReader()
    assert reader
