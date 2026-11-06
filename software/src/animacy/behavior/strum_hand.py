"""
DaBones

Strum hand behaviors.

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

class StrumHandBehavior(Behavior):
    """Strum hand behaviors."""

    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache, name:str="StrumHand") -> None:
        """Initialize StrumHandBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(port)
        self.next  = next
        self.cache = cache

        # Strum hand has a few setpoints: high, strings 6-1, low
        self.setpoints = [
            Setpoint("6", PositionDriverValue(1180)),
            Setpoint("5", PositionDriverValue(1180)),
            Setpoint("4", PositionDriverValue(1320)),
            Setpoint("3", PositionDriverValue(1405)),
            Setpoint("2", PositionDriverValue(1560)),
            Setpoint("1", PositionDriverValue(1665)),
            Setpoint("low", PositionDriverValue(1760)),

        ]

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        if (isinstance(message, MidiNoteOn) and message.note >= 36  and message.note <=47):
            self.next.process(PerformancePlayTechiqueMessage(timecode=timecode, technique=message.note-36, intensity=127))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiNoteOff) and message.note>= 36  and message.note <= 47):
            self.next.process(PerformancePlayTechiqueMessage(timecode=timecode, technique=message.note-36, intensity=0))
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED        

    def process(self, message:PerformanceDataMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            self._update(message=message, start_index=0, end_index=0)
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformancePlayTechiqueMessage):
            start = [0,0,3,0,2,4,0,1,2,3,4,5]
            end   = [6,3,6,1,3,5,1,2,3,4,5,6]
            self._update(message=message, start_index=start[message.technique], end_index=end[message.technique])
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message:PerformanceDataMessage, start_index: int, end_index: int) -> None:
        """Update the driver with a command."""
        start_value=self.setpoints[start_index].value
        end_value=self.setpoints[end_index].value
        prep_transition = DriverTransition(self.driver, start_value, start_value)
        play_transition = DriverTransition(self.driver, start_value, end_value)

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(prep_transition)
        prep_transition.start_value = position_last_value or self.setpoints[0].value

        # Decide how much time we need
        prep_timecode = 24
        play_timecode = 6
        target_start = max(message.timecode - prep_timecode, position_last_time)

        # Move to the string start, then play through to end string.
        message.events.append(PerformanceEvent(transition=prep_transition, curve=ZeroEndpointAccelerationCurve(), start=target_start, end=message.timecode))
        message.events.append(PerformanceEvent(transition=play_transition, curve=ZeroEndpointAccelerationCurve(), start=message.timecode, end=message.timecode+play_timecode))
        message.timecode = target_start
        #logger.info(f"Strum transition to sp[{start_index}] through sp[{end_index}]@{message.timecode}")
    