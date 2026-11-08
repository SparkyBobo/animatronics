"""
DaBones

MIDI Serial driver.

Copyright (c) 2026 Sparky Bobo
"""

import busio
from animacy.hardware.ports import SerialPort

import logging
logger = logging.getLogger(__name__)

# A midi serial driver.
class MidiSerialDriver:
    """MidiSerial driver."""

    def __init__(self, port: SerialPort) -> None:
        """Initialize MidiSerialDriver."""
        logger.info(f"Initialize MidiSerialDriver@tx={port.txpin},rx={port.rxpin}")
        self._uart = busio.UART(
            tx=port.txpin, 
            rx=port.rxpin, 
            baudrate=port.baudrate, 
            bits=8,
            parity=None,
            stop=1,
            timeout=port.timeout)

    @property
    def uart(self) -> any:
        return self._uart        
