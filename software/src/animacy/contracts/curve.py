"""
Animacy

Curve contracts.

Copyright (c) 2026 Sparky Bobo
"""

# A curve used to computer progress from absolute time.
class TimeCurve:
    """Map a time window to normalized progress."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        """Map an absolute clock time to progress from 0.0 to 1.0."""
        ...