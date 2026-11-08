"""
Animacy

Audio playback.

Copyright (c) 2026 Sparky Bobo
"""

import board
from animacy.contracts.show import ShowContext
from animacy.drivers.audio import AudioDriver
from animacy.hardware.ports import SerialPort
from animacy.characters.performer import PerformerBase
from animacy.behavior.audio import AudioBehavior

import logging
logger = logging.getLogger(__name__)

class Audio(PerformerBase):
    """Audio performer."""

    def __init__(self, context: ShowContext) -> None:
        """Initialize Audio."""
        super().__init__("Audio", 13)

        # Audio has playback
        self.pizero = AudioDriver(SerialPort(name="PiZero", txpin=board.GP8, rxpin=board.GP9, baudrate=115200, timeout=0.02))
        self.playback = AudioBehavior(name="Playback", driver=self.pizero)

        # Register
        context.add_mapping(self)
        context.add_behavior(self.playback)
        context.add_service(self.pizero)
