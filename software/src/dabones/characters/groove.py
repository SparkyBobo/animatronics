"""
DaBones

Groove performer.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.show import ShowContext
from dabones.hardware.ports import Ports
from dabones.drivers.led import LedDriver
from dabones.characters.performer import PerformerBase
from dabones.behavior.eyes import EyesBehavior
from dabones.behavior.rgb import RgbBehavior
from dabones.behavior.fret_hand import FretHandBehavior
from dabones.behavior.pluck_hand import PluckHandBehavior

import logging
logger = logging.getLogger(__name__)

class Groove(PerformerBase):
    """Groove performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize Groove."""
        super().__init__("Groove", 5)

        # Groove has a fret hand, pluck hand, string bend, and foot tap
        #self.string_bend = StringBendBehavior(port=Ports.io0, power=Ports.io1)
        self.fret_hand = FretHandBehavior(port=Ports.io2, next=context.planner_queue, cache=context.planner_cache)
        self.pluck_hand = PluckHandBehavior(primary=Ports.io0, secondary=Ports.io1, next=context.planner_queue, cache=context.planner_cache)
        #self.foottap = FoottapBehaviour(port=Ports.io5)

        # Groove has standard eyes and skull eyes in the bass
        self.led_driver = LedDriver(4)
        self.left_eye = RgbBehavior(self.led_driver, 0, cache=context.planner_cache, name="LeftEye")
        self.right_eye = RgbBehavior(self.led_driver, 1, cache=context.planner_cache, name="RightEye")
        self.left_eye2 = RgbBehavior(self.led_driver, 2, cache=context.planner_cache, name="LeftEye")
        self.right_eye2 = RgbBehavior(self.led_driver, 3, cache=context.planner_cache, name="RightEye")
        self.eyes = EyesBehavior(leds=[self.left_eye, self.right_eye], next=context.planner_queue)
        self.bass_eyes = EyesBehavior(leds=[self.left_eye2, self.right_eye2], next=context.planner_queue)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.fret_hand)
        context.add_behavior(self.pluck_hand)
        context.add_behavior(self.eyes)
        context.add_behavior(self.bass_eyes)

