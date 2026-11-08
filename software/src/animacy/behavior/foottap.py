"""
Animacy

Foottap behaviors.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.behavior.base import Behavior
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.performance import *
from animacy.contracts.setpoint import Setpoint
from animacy.curves.ease import EaseOutCurve
from animacy.curves.instant import InstantCurve
from animacy.drivers.servo import ServoDriver
from animacy.hardware.ports import IOPort

logger = logging.getLogger(__name__)

class FoottapBehaviour(Behavior):
    """Foottap behaviors."""

    def __init__(self, port:IOPort, name:str="FootTap") -> None:
        """Initialize FoottapBehaviour."""
        super().__init__(name)
        self.driver = ServoDriver(name, port)
        # Foottap has a few setpoints: strike (@surface), attack (@apex), and soft attack (half way)
        self.setpoints = [
            Setpoint("strike", PositionDriverValue(85)),
            Setpoint("attack", PositionDriverValue(95)),
            Setpoint("soft", PositionDriverValue(90)),
        ]

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            reset_transition = DriverTransition(self.driver, self.setpoints[0].value, self.setpoints[0].value)
            message.events.append(PerformanceEvent(transition=reset_transition, curve=InstantCurve(), start=message.timecode, end=message.timecode))
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformancePercussionStrikeMessage):
            index = 1 if message.intensity > 64 else 2
            apex = self.setpoints[index].value
            # Start from current and raise to the apex
            raise_transition = DriverTransition(self.driver, self.setpoints[0].value, apex)
            (_, last_time) = self.cache.get(raise_transition)
            message.events.append(PerformanceEvent(transition=raise_transition, curve=EaseOutCurve(), start=last_time, end=message.timecode-1))
            # From the apex to the strike position
            lower_transition = DriverTransition(self.driver, apex, self.setpoints[0].value)
            message.events.append(PerformanceEvent(transition=lower_transition, curve=InstantCurve(), start=message.timecode, end=message.timecode))
            return PerformanceMessageResult.HANDLED

