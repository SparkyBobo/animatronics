"""
DaBones

Addressable RGBW behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from email import message

from email.mime import message

from dabones.drivers.led import LedDriver
from dabones.behavior.rgb import RgbBehavior
from dabones.contracts.color import Color
from dabones.contracts.driver import AddressableDriverTransition, ColorDriverValue
from dabones.contracts.setpoint import Setpoint
from dabones.contracts.performance import *
from dabones.contracts.planner import DriverValueCache

import logging
logger = logging.getLogger(__name__)

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

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        """Process performance message."""
        if isinstance(message, PerformanceEyeMessage):
            logger.info(f"Process performance message {message.id}@{message.timecode}")
            color = Color(red=message.color.red, green=message.color.green, blue=message.color.blue, white=message.color.white)
            start_time=max(0, message.timecode - message.fade)
            self._update(message=message, color=color, intensity=message.intensity, start_time=start_time)
            return PerformanceMessageResult.HANDLED
        return super().process(message)
