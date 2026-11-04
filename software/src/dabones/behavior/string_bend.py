"""
DaBones

String bend behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.hardware.ports import IOPort
from dabones.drivers.onoff import OnOffDriver
from dabones.drivers.servo import ServoDriver
from dabones.behavior.base import Behavior
from dabones.contracts.driver import DriverTransition, PositionDriverValue
from dabones.contracts.setpoint import Setpoint
from dabones.contracts.performance import PerformanceDataMessage, PerformanceResetEventMessage, PerformanceBendNoteMessage
from dabones.pipeline.processor import PerformanceMessageProcessor, PerformanceMessageHandlerResult

import logging
logger = logging.getLogger(__name__)

class StringBendBehavior(Behavior):
    """String bend behaviors."""

    def __init__(self, port:IOPort, power:IOPort, name:str="StringBend") -> None:
        """Initialize NeckBehavior."""
        super().__init__(name)
        self.driver = ServoDriver(name, port)
        self.enable_driver = OnOffDriver(f"{name}_power", power)
        # Sring bend has a two setpoints
        self.setpoints = [
            Setpoint("rest", DriverTransition(self.driver, PositionDriverValue(85), PositionDriverValue(85))),
            Setpoint("max", DriverTransition(self.driver, PositionDriverValue(95), PositionDriverValue(95)))
        ] 

    def process(self, event:PerformanceDataMessage) -> PerformanceMessageHandlerResult:
        if isinstance(event, PerformanceResetEventMessage):
            return PerformanceMessageHandlerResult.HANDLED_CONTINUE
        if isinstance(event, PerformanceBendNoteMessage):
            return PerformanceMessageHandlerResult.HANDLED_STOP
