"""
Animacy

Instant time transform.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.curve import TimeCurve


class InstantCurve(TimeCurve):
    """Always return full progress, regardless of the supplied times."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        return 1.0