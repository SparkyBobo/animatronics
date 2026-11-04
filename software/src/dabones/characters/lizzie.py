"""
DaBones

LizzieB performer.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.show import ShowContext
from dabones.hardware.ports import Ports
from dabones.characters.performer import PerformerBase
from dabones.behavior.mouth import MouthBehavior
from dabones.behavior.neck import NeckBehavior

import logging
logger = logging.getLogger(__name__)

class LizzieB(PerformerBase):
    """LizzieB performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize LizzieB."""
        super().__init__("LizzieB", 2)

        # LizzieB has a mouth and neck
        self.mouth = MouthBehavior(port=Ports.io0, next=context.planner_queue, cache=context.planner_cache)
        self.neck = NeckBehavior(port=Ports.io1, next=context.planner_queue, cache=context.planner_cache)

        # LizzieB has standard eyes 
        #self.led_driver = LedDriver(2)  
        #self.eyes = EyesBehavior(self.led_driver)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.mouth)
        context.add_behavior(self.neck)        

