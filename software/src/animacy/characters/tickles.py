"""
Animacy

Tickles performer.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.behavior.eyes import EyesBehavior
from animacy.behavior.keys_hand import KeysHandBehavior
from animacy.behavior.mouth import MouthBehavior
from animacy.behavior.rgb import RgbBehavior
from animacy.characters.performer import PerformerBase
from animacy.contracts.show import ShowContext
from animacy.drivers.led import LedDriver
from animacy.hardware.ports import Ports

logger = logging.getLogger(__name__)

class Tickles(PerformerBase):
    """Tickles performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize Tickles."""
        super().__init__("Tickles", 7)

        # Tickles has a mouth, keyboard and foot tap
        self.mouth = MouthBehavior(port=Ports.io0, next=context.planner_queue, cache=context.planner_cache)
        self.left = KeysHandBehavior(updown=Ports.io1, slide=Ports.io2, start_note=48, end_note=59, next=context.planner_queue, cache=context.planner_cache, name="Left")
        self.right = KeysHandBehavior(updown=Ports.io3, slide=Ports.io4, start_note=60, end_note=71, next=context.planner_queue, cache=context.planner_cache, name="Right")
        #self.foottap = FoottapBehaviour(port=Ports.io2)

        # Tickles has standard eyes and a translucent bust
        self.led_driver = LedDriver(6)
        self.left_eye = RgbBehavior(self.led_driver, 0, cache=context.planner_cache, name="LeftEye")
        self.right_eye = RgbBehavior(self.led_driver, 1, cache=context.planner_cache, name="RightEye")
        self.eyes = EyesBehavior(leds=[self.left_eye, self.right_eye], next=context.planner_queue)

        self.bust1 = RgbBehavior(self.led_driver, 2, cache=context.planner_cache, name="Bust1")
        self.bust2 = RgbBehavior(self.led_driver, 3, cache=context.planner_cache, name="Bust2")
        self.bust3 = RgbBehavior(self.led_driver, 4, cache=context.planner_cache, name="Bust3")
        self.bust4 = RgbBehavior(self.led_driver, 5, cache=context.planner_cache, name="Bust4")
        self.bust = EyesBehavior(leds=[self.bust1, self.bust2, self.bust3, self.bust4], next=context.planner_queue)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.mouth)
        context.add_behavior(self.left)
        context.add_behavior(self.right)
        context.add_behavior(self.eyes)
        context.add_behavior(self.bust)
