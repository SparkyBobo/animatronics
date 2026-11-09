"""
Animacy

String bend behaviors.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.behavior.base import Behavior
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.performance import (
    PerformanceBendNoteMessage,
    PerformanceDataMessage,
    PerformanceResetEventMessage,
)
from animacy.contracts.setpoint import Setpoint
from animacy.drivers.onoff import OnOffDriver
from animacy.drivers.servo import ServoDriver
from animacy.hardware.ports import IOPort
from animacy.pipeline.processor import (
    PerformanceMessageHandlerResult,
)

logger = logging.getLogger(__name__)


class StringBendBehavior(Behavior):
    """String bend behaviors."""

    def __init__(self, port: IOPort, power: IOPort, name: str = "StringBend") -> None:
        """Initialize NeckBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(name, port)
        self.enable_driver = OnOffDriver(f"{name}_power", power)
        # Sring bend has a two setpoints
        self.setpoints = [
            Setpoint(
                "rest",
                DriverTransition(
                    self.driver, PositionDriverValue(85), PositionDriverValue(85)
                ),
            ),
            Setpoint(
                "max",
                DriverTransition(
                    self.driver, PositionDriverValue(95), PositionDriverValue(95)
                ),
            ),
        ]

    def process(self, event: PerformanceDataMessage) -> PerformanceMessageHandlerResult:
        if isinstance(event, PerformanceResetEventMessage):
            return PerformanceMessageHandlerResult.HANDLED_CONTINUE
        if isinstance(event, PerformanceBendNoteMessage):
            return PerformanceMessageHandlerResult.HANDLED_STOP
