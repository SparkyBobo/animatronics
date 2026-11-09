"""
Animacy

MIDI Serial driver.

Copyright (c) 2026 Sparky Bobo
"""

import busio

from animacy.hardware.ports import SerialPort
from animacy.utils.logging import INFO, log


# A midi serial driver.
class MidiSerialDriver:
    """MidiSerial driver."""

    def __init__(self, port: SerialPort) -> None:
        """Initialize MidiSerialDriver."""
        log(5, INFO)
        self._uart = busio.UART(
            tx=port.txpin,
            rx=port.rxpin,
            baudrate=port.baudrate,
            bits=8,
            parity=None,
            stop=1,
            timeout=port.timeout,
        )

    @property
    def uart(self) -> any:
        return self._uart
