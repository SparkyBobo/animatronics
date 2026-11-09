"""
Animacy

Analog driver.

Copyright (c) 2026 Sparky Bobo
"""

import logging

from animacy.hardware.ports import IOPort

logger = logging.getLogger(__name__)


# An analog driver.
class AnalogDriver:
    """Analog driver."""

    def __init__(self, port: IOPort) -> None:
        """Initialize AnalogDriver."""
        self.port = port
