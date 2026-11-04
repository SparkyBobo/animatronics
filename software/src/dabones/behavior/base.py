"""
DaBones

Base behavior class.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.performance import PerformanceMessage, PerformanceMessageResult

import logging
logger = logging.getLogger(__name__)

class Behavior:
    """Base behavior class."""

    def __init__(self, name: str="UndefinedBehaviour") -> None:
        """Initialize Behavior."""
        self.name = name

    def process(self, event:PerformanceMessage) -> PerformanceMessageResult:
        pass

