"""
DaBones

Serial Host for MIDI messages.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.drivers.midi_serial import MidiSerialDriver
from animacy.hardware.ports import Ports
import adafruit_midi

import logging
logger = logging.getLogger(__name__)

class MidiSerialPort:
    """Reads MIDI messages from serial."""

    def __init__(self) -> None:
        """Initialize MidiSerialPort."""
        self.driver = MidiSerialDriver(Ports.midi)
        self._midi = adafruit_midi.MIDI(midi_in=self.driver.uart, midi_out=self.driver.uart) 

    @property
    def device(self) -> any:
        return self._midi


