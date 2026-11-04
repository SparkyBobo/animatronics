"""
DaBones

Audio playback driver.

Copyright (c) 2026 Sparky Bobo
"""

import busio
import time
import dabones.contracts.driver
import dabones.contracts.service
import dabones.hardware.ports

import logging
logger = logging.getLogger(__name__)

class AudioDriver:
    """Control a Pi Zero through its Linux serial terminal."""

    def __init__(self, port: dabones.hardware.ports.SerialPort) -> None:
        """Initialize AudioDriver."""
        logger.info(f"Initialize AudioDriver @tx={port.txpin}, rx={port.rxpin}")
        self.uart = busio.UART(
            tx=port.txpin,
            rx=port.rxpin,
            baudrate=port.baudrate,
            bits=8,
            parity=None,
            stop=1,
            timeout=port.timeout,
        )
        self.last_activity = time.monotonic()
        self.constraints = dabones.contracts.driver.DriverConstraints(
            dabones.contracts.driver.IntensityDriverValue(0),
            dabones.contracts.driver.IntensityDriverValue(255),
            0.0,
            0.0,
        )

    def process(self, transition: dabones.contracts.driver.DriverTransition) -> dabones.contracts.driver.DriverTransitionResult:
        if isinstance(transition.end_value, dabones.contracts.driver.AudioDriverValue):
            logger.info(f"Audio PiZero command:{transition.end_value.command}")
            self._send_line(transition.end_value.command)

    def constraints_for(self, value: dabones.contracts.driver.DriverValue) -> dabones.contracts.driver.DriverConstraints:
        """Return constraints for the given typed driver value."""
        if isinstance(value, dabones.contracts.driver.AudioDriverValue):
            return self.constraints
        raise ValueError(f"Unsupported driver value type: {type(value)}")

    def service(self) -> dabones.contracts.service.ServiceResult:
        """Process incoming terminal output; call frequently."""
        if (self.last_activity + 5.0) < time.monotonic():
            logger.info("Ping Audio PiZero")
            self._send_line("PING")
            self.last_activity = time.monotonic()

        data = self.uart.readline()
        if not data:
            return dabones.contracts.service.ServiceResult.IDLE
        text = data.decode("ascii").strip()
        logger.info(f"Audio PiZero state:{text}")
        return dabones.contracts.service.ServiceResult.ACTIVITY

    def _send_line(self, text):
        self.uart.write((text + "\r\n").encode())
