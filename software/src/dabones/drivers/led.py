"""
DaBones

Led driver.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.contracts.color
import dabones.contracts.driver
import dabones.hardware.ports
import neopixel

import logging
logger = logging.getLogger(__name__)

class LedDriver:
    """Led driver."""

    def __init__(self, count: int = 2) -> None:
        """Initialize LedDriver."""
        self.pixel_count = count
        self.pixels = neopixel.NeoPixel(dabones.hardware.ports.Ports.led.pin, self.pixel_count)
        self.color_constraints = dabones.contracts.driver.DriverConstraints(
            dabones.contracts.driver.ColorDriverValue(dabones.contracts.color.Color(0, 0, 0)),
            dabones.contracts.driver.ColorDriverValue(dabones.contracts.color.Color(255, 255, 255)),
            0.0,
            0.0,
        )
        self.intensity_constraints = dabones.contracts.driver.DriverConstraints(
            dabones.contracts.driver.IntensityDriverValue(0),
            dabones.contracts.driver.IntensityDriverValue(255),
            0.0,
            0.0,
        )

    def process(self, transition: dabones.contracts.driver.DriverTransition) -> dabones.contracts.driver.DriverTransitionResult:
        target = transition.start_value.interpolate(transition.end_value, transition.progress)
        if isinstance(target, dabones.contracts.driver.ColorDriverValue):
            self.pixels[transition.address] = (target.color.red, target.color.green, target.color.blue)
        elif isinstance(target, dabones.contracts.driver.IntensityDriverValue):
            self.pixels.brightness = target.intensity / 255.0
        self.pixels.show()

    def constraints_for(self, value: dabones.contracts.driver.DriverValue) -> dabones.contracts.driver.DriverConstraints:
        """Return constraints for the given typed driver value."""
        if isinstance(value, dabones.contracts.driver.ColorDriverValue):
            return self.color_constraints
        if isinstance(value, dabones.contracts.driver.IntensityDriverValue):
            return self.intensity_constraints
        raise ValueError(f"Unsupported driver value type: {type(value)}")
