"""
DaBones

Percussion behaviors.

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

class PercussionBehavior(Behavior):
    """Percussion behaviors."""

    def __init__(self, port:IOPort, note:int, setpoints: list[Setpoint], next:PerformanceMessageProcessor, cache: DriverValueCache, name:str) -> None:
        """Initialize PercussionBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(port)
        self.next  = next
        self.cache = cache
        self.note = note
        self.setpoints = setpoints

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        if (isinstance(message, MidiNoteOn) and message.note == self.note):
            self.next.process(PerformancePercussionStrikeMessage(timecode=timecode, target=self.name, intensity=message.velocity))
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiNoteOff) and message.note == self.note):
            return MidiMessageResult.HANDLED
        if (isinstance(message, MidiPitchBend)):
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED        

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            self._update(message, attack_pos=self.setpoints[2].value)
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformancePercussionStrikeMessage):
            self._update(message, attack_pos=self.setpoints[0].value)
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message:PerformanceDataMessage, attack_pos: PositionDriverValue) -> None:
        """Update the driver with a command."""
        prep_transition = DriverTransition(self.driver, attack_pos, attack_pos)
        play_transition = DriverTransition(self.driver, attack_pos, self.setpoints[2].value)

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(prep_transition)
        prep_transition.start_value = position_last_value or self.setpoints[2].value

        # Decide how much time we need
        prep_timecode = 24
        play_timecode = 6
        target_start = max(message.timecode - prep_timecode, position_last_time)
        target_play = max(message.timecode - play_timecode, target_start)

        # Move to the string start, then play through to end string.
        message.events.append(PerformanceEvent(transition=prep_transition, curve=ZeroEndpointAccelerationCurve(), start=target_start, end=target_play))
        message.events.append(PerformanceEvent(transition=play_transition, curve=ZeroEndpointAccelerationCurve(), start=target_play, end=message.timecode))
        logger.info(f"Percusion strike for {self.name}@{message.timecode}")  


class BassPercussionBehavior(PercussionBehavior):
    """Bass behaviors."""
    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache) -> None:
        # Bass has a few setpoints: strike (@surface), attack (@apex), and soft attack (half way)
        setpoints = [
            Setpoint("attack", PositionDriverValue(95)),
            Setpoint("soft", PositionDriverValue(90)),
            Setpoint("strike", PositionDriverValue(85)),
        ]
        super().__init__(port=port, note=36, setpoints=setpoints, next=next, cache=cache, name="Bass")

class SnarePercussionBehavior(PercussionBehavior):
    """Snare behaviors."""
    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache) -> None:
        # Snare has a few setpoints: strike (@surface), attack (@apex), and soft attack (half way)
        setpoints = [
            Setpoint("attack", PositionDriverValue(95)),
            Setpoint("soft", PositionDriverValue(90)),
            Setpoint("strike", PositionDriverValue(85)),
        ]
        super().__init__(port=port, note=38, setpoints=setpoints, next=next, cache=cache, name="Snare")

class HitHatPercussionBehavior(PercussionBehavior):
    """Hihat behaviors."""
    def __init__(self, port:IOPort, next:PerformanceMessageProcessor, cache: DriverValueCache) -> None:
        # Hihat has a few setpoints: strike (@surface), attack (@apex), and soft attack (half way)
        setpoints = [
            Setpoint("attack", PositionDriverValue(95)),
            Setpoint("soft", PositionDriverValue(90)),
            Setpoint("strike", PositionDriverValue(85)),
        ]
        super().__init__(port=port, note=42, setpoints=setpoints, next=next, cache=cache, name="Hihat")


