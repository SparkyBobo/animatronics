"""
Animacy

Eyes behaviors.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.behavior.base import Behavior
from animacy.behavior.rgb import RgbBehavior
from animacy.contracts.midi import *
from animacy.contracts.performance import *
from animacy.contracts.planner import *

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
        if isinstance(message, (PerformanceResetEventMessage, PerformanceEyeMessage)):
            for led in self.leds:
                led.process(message)
            if isinstance(message, PerformanceEyeMessage) and message.fade > 0:
                message.timecode = max(0, message.timecode - message.fade)
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED