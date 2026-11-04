"""
DaBones

Beats performer.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.show import ShowContext
from dabones.hardware.ports import Ports
from dabones.drivers.led import LedDriver
from dabones.characters.performer import PerformerBase
from dabones.behavior.eyes import EyesBehavior
from dabones.behavior.rgb import RgbBehavior
from dabones.behavior.mouth import MouthBehavior
from dabones.behavior.percussion import BassPercussionBehavior, SnarePercussionBehavior, HitHatPercussionBehavior

import logging
logger = logging.getLogger(__name__)

class Beats(PerformerBase):
    """Beats performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize Beats."""
        super().__init__("Beats", 4)

        # Beats has a mouth, bass foot, cymbal foot, and snare arm
        self.mouth = MouthBehavior(port=Ports.io0, next=context.planner_queue, cache=context.planner_cache)
        self.bass = BassPercussionBehavior(port=Ports.io1, next=context.planner_queue, cache=context.planner_cache)
        self.snare = SnarePercussionBehavior(port=Ports.io2, next=context.planner_queue, cache=context.planner_cache)
        self.hihat = HitHatPercussionBehavior(port=Ports.io3, next=context.planner_queue, cache=context.planner_cache)

        # Beats has standard eyes
        self.led_driver = LedDriver(2)
        self.left_eye = RgbBehavior(self.led_driver, 1, cache=context.planner_cache, name="LeftEye")
        self.right_eye = RgbBehavior(self.led_driver, 2, cache=context.planner_cache, name="RightEye")
        self.eyes = EyesBehavior(leds=[self.left_eye, self.right_eye], next=context.planner_queue)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.mouth)
        context.add_behavior(self.bass)
        context.add_behavior(self.snare)
        context.add_behavior(self.hihat)
        context.add_behavior(self.eyes)
