"""
Animacy

Led driver.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import *
from animacy.hardware.ports import Ports
import neopixel

import logging
logger = logging.getLogger(__name__)

# An LED (NeoPixel) driver.
class LedDriver:
    """Led driver."""

    def __init__(self, count:int = 2) -> None:
        """Initialize LedDriver."""
        # Neopixels
        self.pixel_count = count
        self.pixels = neopixel.NeoPixel(Ports.led.pin, self.pixel_count)
        self.color_constraints = DriverConstraints(ColorDriverValue(Color(0, 0, 0)), ColorDriverValue(Color(255, 255, 255)), 0.0, 0.0)
        self.intensity_constraints = DriverConstraints(IntensityDriverValue(0), IntensityDriverValue(255), 0.0, 0.0)

    def process(self, transition: DriverTransition) -> DriverTransitionResult:
        target = transition.start_value.interpolate(transition.end_value, transition.progress)
        if isinstance(target, ColorDriverValue):
            self.pixels[transition.address] = (target.color.red, target.color.green, target.color.blue)
        elif isinstance(target, IntensityDriverValue):
            self.pixels.brightness = target.intensity / 255.0
        self.pixels.show()

    def constraints_for(self, value: DriverValue) -> DriverConstraints:
        """Return constraints for the given typed driver value."""
        if isinstance(value, ColorDriverValue):
            return self.color_constraints
        elif isinstance(value, IntensityDriverValue):
            return self.intensity_constraints
        else:
            raise ValueError(f"Unsupported driver value type: {type(value)}")
