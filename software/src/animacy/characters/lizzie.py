"""
Animacy

LizzieB performer.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.behavior.mouth import MouthBehavior
from animacy.behavior.neck import NeckBehavior
from animacy.characters.performer import PerformerBase
from animacy.contracts.show import ShowContext
from animacy.hardware.ports import Ports

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

