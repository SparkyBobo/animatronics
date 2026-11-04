"""
DaBones

Eyes behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.midi import *
from dabones.contracts.performance import *
from dabones.contracts.planner import *
from dabones.behavior.base import Behavior
from dabones.behavior.rgb import RgbBehavior
from dabones.contracts.driver import DriverTransition, PositionDriverValue
from dabones.contracts.setpoint import Setpoint
from dabones.curves.ease import ZeroEndpointAccelerationCurve

import logging
logger = logging.getLogger(__name__)

class EyesBehavior(Behavior):
    """Eyes behaviors."""

    def __init__(self, leds: list[RgbBehavior], next:PerformanceMessageProcessor, name:str="Eyes") -> None:
        """Initialize EyesBehavior."""
        super().__init__(name)
        self.leds = leds
        self.next = next

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        if (isinstance(message, MidiNoteOn) and message.note == 29):
            self.next.process(PerformanceEyeMessage(timecode=timecode, color=Color(), intensity=message.velocity, fade=0))
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED    

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage) or isinstance(message, PerformanceEyeMessage):
            for led in self.leds:
                led.process(message)
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED