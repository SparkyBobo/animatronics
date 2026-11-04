"""
DaBones

Servo driver.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.contracts.driver
import dabones.hardware.ports
import pwmio

import logging
logger = logging.getLogger(__name__)

class ServoDriver:
    """Servo driver."""

    def __init__(self, port: dabones.hardware.ports.IOPort) -> None:
        """Initialize ServoDriver."""
        logger.info(f"Initialize ServoDriver@{port.pin}")
        self.port = port
        self.pwm = pwmio.PWMOut(port.pin, frequency=50)
        self.total_period_us = 20000
        self.constraints = dabones.contracts.driver.DriverConstraints(
            dabones.contracts.driver.PositionDriverValue(800),
            dabones.contracts.driver.PositionDriverValue(2200),
            0.0,
            0.0,
        )

    def process(self, transition: dabones.contracts.driver.DriverTransition) -> dabones.contracts.driver.DriverTransitionResult:
        target = transition.start_value.interpolate(transition.end_value, transition.progress)
        if isinstance(target, dabones.contracts.driver.PositionDriverValue):
            duty_ratio = target.position / self.total_period_us
            self.pwm.duty_cycle = int(duty_ratio * 65535)

    def constraints_for(self, value: dabones.contracts.driver.DriverValue) -> dabones.contracts.driver.DriverConstraints:
        """Return constraints for the given typed driver value."""
        if isinstance(value, dabones.contracts.driver.PositionDriverValue):
            return self.constraints
        raise ValueError(f"Unsupported driver value type: {type(value)}")
