"""
DaBones

Linear time transform.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.curve import TimeCurve
from animacy.curves._progress import linear_progress


class LinearCurve(TimeCurve):
    """Map a time window linearly to normalized progress."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        """Return current clock time as a clamped fraction of the time window."""
        return linear_progress(start_time, end_time, current_time)