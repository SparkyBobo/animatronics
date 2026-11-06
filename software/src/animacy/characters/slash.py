"""
DaBones

Slash performer.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.show import ShowContext
from animacy.hardware.ports import Ports
from animacy.drivers.led import LedDriver
from animacy.characters.performer import PerformerBase
from animacy.behavior.eyes import EyesBehavior
from animacy.behavior.eyes import RgbBehavior
from animacy.behavior.fret_hand import FretHandBehavior
from animacy.behavior.strum_hand import StrumHandBehavior

import logging
logger = logging.getLogger(__name__)

class Slash(PerformerBase):
    """Slash performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize Slash."""
        super().__init__("Slash", 6)

        # Slash has a fret hand, strum hand, string bend, and foot tap
        #self.string_bend = StringBendBehavior(port=Ports.io0, power=Ports.io1)
        self.fret_hand = FretHandBehavior(port=Ports.io2, next=context.planner_queue, cache=context.planner_cache)
        self.strum_hand = StrumHandBehavior(port=Ports.io3, next=context.planner_queue, cache=context.planner_cache)
        #self.foottap = FoottapBehaviour(port=Ports.io4)   

        # Slash has standard eyes 
        self.led_driver = LedDriver(2)
        self.left_eye = RgbBehavior(self.led_driver, 0, cache=context.planner_cache, name="LeftEye")
        self.right_eye = RgbBehavior(self.led_driver, 1, cache=context.planner_cache, name="RightEye")
        self.eyes = EyesBehavior(leds=[self.left_eye, self.right_eye], next=context.planner_queue)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.fret_hand)
        context.add_behavior(self.strum_hand)
        context.add_behavior(self.eyes)
