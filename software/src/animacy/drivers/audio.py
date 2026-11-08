"""
Animacy

Audio playback driver.

Copyright (c) 2026 Sparky Bobo
"""

import busio
import time
from animacy.contracts.driver import *
from animacy.contracts.service import *
from animacy.hardware.ports import SerialPort

from animacy.utils.logging import INFO, log

# An audio playback driver.
class AudioDriver(Service):
    """Control a Pi Zero through its Linux serial terminal."""

    def __init__(self, port: SerialPort) -> None:
        """Initialize AudioDriver."""
        log(5, INFO)
        self.uart = busio.UART(
            tx=port.txpin,
            rx=port.rxpin,
            baudrate=port.baudrate,
            bits=8,
            parity=None,
            stop=1,
            timeout=port.timeout)

        self.last_activity = time.monotonic()
        self.constraints = DriverConstraints(IntensityDriverValue(0), IntensityDriverValue(255), 0.0, 0.0)

    def process(self, transition: DriverTransition) -> DriverTransitionResult:
        if isinstance(transition.end_value, AudioDriverValue):
            log(1302, INFO, transition.end_value.command)
            self._send_line(transition.end_value.command)

    def constraints_for(self, value: DriverValue) -> DriverConstraints:
        """Return constraints for the given typed driver value."""
        if isinstance(value, AudioDriverValue):
            return self.constraints
        else:
            raise ValueError(f"Unsupported driver value type: {type(value)}")

    def service(self) -> ServiceResult:
        """Process incoming terminal output; call frequently."""
        # If we are disconnected, try to get a response.
        if ((self.last_activity + 5.0) < time.monotonic()):
            log(1303, INFO)
            self._send_line("PING")
            self.last_activity = time.monotonic()

        # Read the response.
        data = self.uart.readline()
        if not data:
            return ServiceResult.IDLE

        text = data.decode("ascii").strip()
        log(1304, INFO, text)
        return ServiceResult.ACTIVITY

    def _send_line(self, text):
        self.uart.write((text + "\r\n").encode())
