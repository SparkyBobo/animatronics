"""
Animacy

Addressable RGBW behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.behavior.rgb import RgbBehavior
from animacy.contracts.color import Color
from animacy.contracts.performance import (
    PerformanceEyeMessage,
    PerformanceMessage,
    PerformanceMessageResult,
)
from animacy.contracts.planner import DriverValueCache
from animacy.drivers.led import LedDriver
from animacy.utils.logging import INFO, log


class RgbwBehavior(RgbBehavior):
    """Addressable RGBW LED behaviors."""

    def __init__(
        self,
        cache: DriverValueCache,
        driver: LedDriver,
        address: int,
        name: str,
    ) -> None:
        """Initialize RgbwBehavior."""
        super().__init__(driver=driver, address=address, name=name, cache=cache)
        self.color = Color(white=0)

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        """Process performance message."""
        if isinstance(message, PerformanceEyeMessage):
            log(1, INFO, message.id, message.timecode)
            color = Color(
                red=message.color.red,
                green=message.color.green,
                blue=message.color.blue,
                white=message.color.white,
            )
            start_time = max(0, message.timecode - message.fade)
            self._update(
                message=message,
                color=color,
                intensity=message.intensity,
                start_time=start_time,
            )
            return PerformanceMessageResult.HANDLED
        return super().process(message)
