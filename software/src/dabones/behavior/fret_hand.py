"""
DaBones

Fret hand behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.midi import *
from dabones.contracts.performance import *
from dabones.contracts.planner import *
from dabones.hardware.ports import IOPort
from dabones.drivers.servo import ServoDriver
from dabones.behavior.base import Behavior
from dabones.contracts.driver import DriverTransition, PositionDriverValue
from dabones.contracts.setpoint import Setpoint
from dabones.curves.ease import ZeroEndpointAccelerationCurve

import logging
logger = logging.getLogger(__name__)

class FretHandBehavior(Behavior):
    """Fret hand behaviors."""

    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache, name:str="FretHand") -> None:
        """Initialize FretHandBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(port)
        self.next  = next
        self.cache = cache

        # Fret hand has a two setpoints: low and high
        self.setpoints = [
            Setpoint("low", PositionDriverValue(980)),
            Setpoint("high", PositionDriverValue(1620)),
        ]

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        if (isinstance(message, MidiNoteOn) and message.note >= 48 and message.note <= 71):
            self.next.process(PerformanceNeckPositionMessage(timecode=timecode, position=message.note - 48, intensity=message.velocity))
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            self._update(message, position=0)
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformanceNeckPositionMessage):
            self._update(message, position=message.position)
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message:PerformanceDataMessage, position: int) -> None:
        """Update the driver with a command."""
        # Scale the position to abs(0.0-1.0)
        progress = position / 23.0
        target = (self.setpoints[0].value).interpolate(self.setpoints[1].value, progress)
        fret_transition = DriverTransition(self.driver, target, target)

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(fret_transition)
        fret_transition.start_value = position_last_value or self.setpoints[0].value

        # Decide how much time we need
        prep_timecode = 24
        target_start = max(message.timecode - prep_timecode, position_last_time)
        message.events.append(PerformanceEvent(transition=fret_transition, curve=ZeroEndpointAccelerationCurve(), start=target_start, end=message.timecode))
        message.timecode = target_start
        #logger.info(f"Fret transition to {target}@{message.timecode}")
