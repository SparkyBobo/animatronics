"""
Animacy

Servo driver.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import *
from animacy.hardware.ports import IOPort
from pwmio import PWMOut

from animacy.utils.logging import INFO, log

# A servo driver.
class ServoDriver:
    """Servo driver."""

    def __init__(self, port:IOPort) -> None:
        """Initialize ServoDriver."""
        log(5, INFO)
        self.port = port
        self.pwm = PWMOut(port.pin, frequency=50)
        self.total_period_us = 20000  # 20ms in microseconds
        self.constraints = DriverConstraints(PositionDriverValue(800), PositionDriverValue(2200), 0.0, 0.0)

    def process(self, transition: DriverTransition) -> DriverTransitionResult:
        target = transition.start_value.interpolate(transition.end_value, transition.progress)
        if isinstance(target, PositionDriverValue):
            #logger.info(f"ServoDriver to {target}")
            duty_ratio = target.position / self.total_period_us
            self.pwm.duty_cycle = int(duty_ratio * 65535)            

    def constraints_for(self, value: DriverValue) -> DriverConstraints:
        """Return constraints for the given typed driver value."""
        if isinstance(value, PositionDriverValue):
            return self.constraints
        else:
            raise ValueError(f"Unsupported driver value type: {type(value)}")