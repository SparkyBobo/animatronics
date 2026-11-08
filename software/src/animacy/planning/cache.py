"""
DaBones

Driver value cache.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import DriverTransition, DriverValue

import logging
logger = logging.getLogger(__name__)

class PlanningCache:
    """Cache values by driver, value type, and optional address."""

    def __init__(self) -> None:
        """Initialize the value cache."""
        self.cache = {}

    def get(self, transition: DriverTransition) -> tuple[DriverValue | None, int]:
        """Get the latest value and timecode for this driver's key."""
        return self.cache.get(transition.key, (None, 0))

    def update(self, transition: DriverTransition, timecode: int) -> None:
        """Update the cached value if its timecode is newer."""
        key = transition.key
        _, last_timecode = self.cache.get(key, (None, 0))
        if timecode > last_timecode:
            self.cache[key] = (transition.end_value, timecode)
