"""
Animacy

Ease time transforms.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.curve import TimeCurve
from animacy.curves._progress import linear_progress


class EaseInCurve(TimeCurve):
    """Accelerate from zero progress into the interval."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        linear = linear_progress(start_time, end_time, current_time)
        return linear * linear


class EaseOutCurve(TimeCurve):
    """Decelerate toward full progress at the end of the interval."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        linear = linear_progress(start_time, end_time, current_time)
        remaining = 1.0 - linear
        return 1.0 - remaining * remaining


class EaseInOutTransform(TimeCurve):
    """Combine quadratic ease-in and ease-out symmetrically."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        linear = linear_progress(start_time, end_time, current_time)
        if linear < 0.5:
            return 2.0 * linear * linear
        remaining = 1.0 - linear
        return 1.0 - 2.0 * remaining * remaining


class ZeroEndpointVelocityCurve(TimeCurve):
    """Cubic smoothstep with zero velocity at both endpoints."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        linear = linear_progress(start_time, end_time, current_time)
        return linear * linear * (3.0 - 2.0 * linear)


class ZeroEndpointAccelerationCurve(TimeCurve):
    """Quintic smootherstep with zero velocity and acceleration at both endpoints."""

    def progress(
        self,
        start_time: int,
        end_time: int,
        current_time: int,
    ) -> float:
        linear = linear_progress(start_time, end_time, current_time)
        return linear**3 * (linear * (linear * 6.0 - 15.0) + 10.0)
