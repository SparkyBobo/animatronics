"""
Animacy

Joey performer.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.show import ShowContext
from animacy.hardware.ports import Ports
from animacy.characters.performer import PerformerBase
from animacy.behavior.mouth import MouthBehavior
from animacy.behavior.neck import NeckBehavior

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

