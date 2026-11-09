"""
Animacy

Shared time-transform progress helpers.

Copyright (c) 2026 Sparky Bobo
"""


def linear_progress(
    start_time: int,
    end_time: int,
    current_time: int,
) -> float:
    """Map a time window to clamped linear progress."""
    duration = end_time - start_time
    if duration <= 0:
        return 1.0 if current_time >= end_time else 0.0
    if current_time <= start_time:
        return 0.0
    if current_time >= end_time:
        return 1.0
    return (current_time - start_time) / duration
