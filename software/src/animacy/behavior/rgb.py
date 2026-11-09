"""
Animacy

Addressable RGB behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.behavior.base import Behavior
from animacy.contracts.color import Color
from animacy.contracts.driver import (
    AddressableDriverTransition,
    ColorDriverValue,
    DriverTransition,
    IntensityDriverValue,
)
from animacy.contracts.performance import (
    PerformanceDataMessage,
    PerformanceEvent,
    PerformanceEyeMessage,
    PerformanceMessage,
    PerformanceMessageResult,
    PerformanceResetEventMessage,
)
from animacy.contracts.planner import DriverValueCache
from animacy.curves.linear import LinearCurve
from animacy.drivers.led import LedDriver
from animacy.utils.logging import INFO, CatalogLogger

logger = CatalogLogger(__name__)


class RgbBehavior(Behavior):
    """Addressable RGB LED behaviors."""

    def __init__(
        self,
        driver: LedDriver,
        address: int,
        cache: DriverValueCache,
        name: str,
    ) -> None:
        """Initialize RgbBehavior."""
        super().__init__(name)
        self.cache = cache
        self.driver = driver
        self.address = address

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        """Process performance events."""
        if isinstance(message, PerformanceResetEventMessage):
            self._update(
                message=message, color=Color(), intensity=0, start_time=message.timecode
            )
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceEyeMessage):
            red = max(message.color.red, message.color.white)
            green = max(message.color.green, message.color.white)
            blue = max(message.color.blue, message.color.white)
            start_time = max(0, message.timecode - message.fade)
            self._update(
                message=message,
                color=Color(red=red, green=green, blue=blue),
                intensity=message.intensity,
                start_time=start_time,
            )
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def _update(
        self,
        message: PerformanceDataMessage,
        color: Color,
        intensity: int,
        start_time: int,
    ) -> None:
        """Update the driver with the current color and intensity."""
        color_transition = AddressableDriverTransition(
            self.driver,
            ColorDriverValue(Color()),
            ColorDriverValue(color),
            address=self.address,
        )
        (color_last_value, _) = self.cache.get(color_transition)
        color_transition.start_value = (
            color_last_value
            if color_last_value is not None
            else ColorDriverValue(Color())
        )
        message.events.append(
            PerformanceEvent(
                transition=color_transition,
                curve=LinearCurve(),
                start=start_time,
                end=message.timecode,
            )
        )
        logger.log(
            1011,
            INFO,
            color_transition.start_value,
            start_time,
            color_transition.end_value,
            message.timecode,
            self.address,
        )

        intensity_transition = DriverTransition(
            self.driver, IntensityDriverValue(0), IntensityDriverValue(intensity)
        )
        (intensity_last_value, _) = self.cache.get(intensity_transition)
        intensity_transition.start_value = (
            intensity_last_value
            if intensity_last_value is not None
            else IntensityDriverValue(0)
        )
        message.events.append(
            PerformanceEvent(
                transition=intensity_transition,
                curve=LinearCurve(),
                start=start_time,
                end=message.timecode,
            )
        )
        logger.log(
            1012,
            INFO,
            intensity_transition.start_value,
            start_time,
            intensity_transition.end_value,
            message.timecode,
            self.address,
        )
