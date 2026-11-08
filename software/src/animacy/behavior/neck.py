"""
Animacy

Neck behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.contracts.performance import *
from animacy.contracts.planner import *
from animacy.hardware.ports import IOPort
from animacy.drivers.servo import ServoDriver
from animacy.behavior.base import Behavior
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.setpoint import Setpoint
from animacy.curves.ease import ZeroEndpointAccelerationCurve

import logging
logger = logging.getLogger(__name__)

class NeckBehavior(Behavior):
    """Neck behaviors."""

    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache, name:str="Mouth") -> None:
        """Initialize NeckBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(port)
        self.next  = next
        self.cache = cache        

        # Neck has a few setpoints: left, center, right
        self.setpoints = [
            Setpoint("left", PositionDriverValue(900)),
            Setpoint("center", PositionDriverValue(1720)),
            Setpoint("right", PositionDriverValue(2200)),
        ]  

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        if (isinstance(message, MidiNoteOn) and message.note == 26):
            self.next.process(PerformanceNeckPositionMessage(timecode=timecode, intensity=-message.velocity))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiNoteOff) and message.note == 26):
            self.next.process(PerformanceNeckPositionMessage(timecode=timecode, intensity=0))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiNoteOn) and message.note == 28):
            self.next.process(PerformanceNeckPositionMessage(timecode=timecode, intensity=message.velocity))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiNoteOff) and message.note == 28):
            self.next.process(PerformanceNeckPositionMessage(timecode=timecode, intensity=0))
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            self._update(message, intensity=0)
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformanceNeckPositionMessage):
            self._update(message, intensity=message.intensity )
            return PerformanceMessageResult.HANDLED

    def _update(self, message:PerformanceDataMessage, intensity: int) -> None:
        """Update the driver with a command."""
        # Scale the position to abs(0.0-1.0)
        progress = abs(intensity / 127.0)
        max_position = self.setpoints[0].value if intensity < 0 else self.setpoints[2].value
        target = self.setpoints[1].value.interpolate(max_position, progress)
        neck_transition = DriverTransition(self.driver, target, target)

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(neck_transition)
        neck_transition.start_value = position_last_value or self.setpoints[1].value

        # Decide how much time we need
        desiered_time = 24
        target_start = max(message.timecode - desiered_time, position_last_time)
        message.events.append(PerformanceEvent(transition=neck_transition, curve=ZeroEndpointAccelerationCurve(), start=target_start, end=message.timecode))
        #logger.info(f"Neck transition to {target}@{message.timecode}")        
