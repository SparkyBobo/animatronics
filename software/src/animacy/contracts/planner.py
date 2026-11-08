"""
Animacy

Planning contracts.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import DriverTransition, DriverValue

# A cache of driver values representing that last known/planned position.
class DriverValueCache:
    """Stores the latest planned driver value and time for each driver key."""

    def get(self, transition: DriverTransition) -> tuple[DriverValue | None, int]:
        """Return the latest value and time for this driver's key."""
        ...

    def update(self, transition: DriverTransition, timecode: int) -> None:
        """Record a value if its timecode is newer than the cached one."""
        ...