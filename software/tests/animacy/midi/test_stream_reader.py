"""
Animacy

Stream reader tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.midi.stream_reader import MidiStreamReader
import mido

def test_reader_init():
    reader = MidiStreamReader()
    assert reader
