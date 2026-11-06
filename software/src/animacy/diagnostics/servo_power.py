"""
DaBones

Servo Power diagnostics.

Copyright (c) 2026 Sparky Bobo
"""

import board
from animacy.drivers.analog import AnalogDriver

import logging
logger = logging.getLogger(__name__)

class ServoPowerDiagnostics:
    """Provides servo power diagnostics."""

    def __init__(self) -> None:
        """Initialize ServoPowerDiagnostics."""
        self.server_power = AnalogDriver(port=board.GP26)
        self.server_current = AnalogDriver(port=board.GP27)

