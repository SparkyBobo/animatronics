"""
Animacy

Mouth and phoneme behaviors.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.behavior.base import Behavior
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.midi import *
from animacy.contracts.performance import *
from animacy.contracts.planner import *
from animacy.contracts.setpoint import Setpoint
from animacy.curves.ease import ZeroEndpointAccelerationCurve
from animacy.drivers.servo import ServoDriver
from animacy.hardware.ports import IOPort

logger = logging.getLogger(__name__)

class MouthBehavior(Behavior):
    """Mouth and phoneme behaviors."""
    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache, name:str="Mouth") -> None:
        """Initialize MouthBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(port)
        self.next  = next
        self.cache = cache

        # Mouth has a few setpoints: closed, soft, normal, scream
        self.setpoints = [
            Setpoint("closed", PositionDriverValue(800)),
            Setpoint("soft", PositionDriverValue(1200)),
            Setpoint("normal", PositionDriverValue(1700)),
            Setpoint("scream", PositionDriverValue(2200)),
        ]

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        if (isinstance(message, MidiNoteOn) and message.note == 29):
            self.next.process(PerformanceSingMessage(timecode=timecode, intensity=message.velocity))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiNoteOff) and message.note == 29):
            self.next.process(PerformanceSingMessage(timecode=timecode, intensity=0))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiPitchBend)):
            #self.next.process(PerformanceBendNoteMessage(timecode=timecode, bend=message.bend))
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            self._update(message, 0)
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformanceBendNoteMessage):
            #logger.info("PerformanceBendNoteMessage")
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformanceSingMessage):
            self._update(message, message.intensity)
            return PerformanceMessageResult.HANDLED

    def _update(self, message:PerformanceDataMessage, intensity: int) -> None:
        """Update the driver with a command."""
        target_index = 0 if intensity == 0 else 1 if intensity < 64 else 2 if intensity < 96 else 3
        target=self.setpoints[target_index].value
        mount_transition = DriverTransition(self.driver, target, target)

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(mount_transition)
        mount_transition.start_value = position_last_value or self.setpoints[0].value

        # Decide how much time we need
        desiered_time = 24
        target_start = max(message.timecode - desiered_time, position_last_time)
        message.events.append(PerformanceEvent(transition=mount_transition, curve=ZeroEndpointAccelerationCurve(), start=target_start, end=message.timecode))
        #logger.info(f"Mouth transition to {target} from sp[{target_index}]@{message.timecode}")
