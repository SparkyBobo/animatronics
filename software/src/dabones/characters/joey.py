"""
DaBones

Joey performer.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.show import ShowContext
from dabones.hardware.ports import Ports
from dabones.characters.performer import PerformerBase
from dabones.behavior.mouth import MouthBehavior
from dabones.behavior.neck import NeckBehavior

import logging
logger = logging.getLogger(__name__)

class Joey(PerformerBase):
    """Joey performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize Joey."""
        super().__init__("Joey", 1)

        # Joey has a mouth, neck, and foot tap
        self.mouth = MouthBehavior(port=Ports.io0, next=context.planner_queue, cache=context.planner_cache)
        self.neck = NeckBehavior(port=Ports.io1, next=context.planner_queue, cache=context.planner_cache)
        #self.foottap = FoottapBehaviour(port=Ports.io2)

        # Joey has standard eyes
        #self.led_driver = LedDriver(2)
        #self.eyes = EyesBehavior(self.led_driver)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.mouth)
        context.add_behavior(self.neck)

