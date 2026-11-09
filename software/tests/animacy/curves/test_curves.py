"""
Animacy

Time curve tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.curves.ease import (
    EaseInCurve,
    EaseInOutTransform,
    EaseOutCurve,
    ZeroEndpointAccelerationCurve,
    ZeroEndpointVelocityCurve,
)
from animacy.curves.instant import InstantCurve
from animacy.curves.linear import LinearCurve


def test_linear_curve_maps_clock_time_to_normalized_progress():
    transform = LinearCurve()
    start = 100
    end = 200

    assert transform.progress(start, end, 100) == 0.0
    assert transform.progress(start, end, 125) == 0.25
    assert transform.progress(start, end, 150) == 0.5
    assert transform.progress(start, end, 200) == 1.0
    assert transform.progress(start, end, 90) == 0.0
    assert transform.progress(start, end, 220) == 1.0
    assert transform.progress(start, start, 99) == 0.0
    assert transform.progress(start, start, 100) == 1.0


def test_ease_in_curve():
    start = 100
    end = 200
    transform = EaseInCurve()

    assert transform.progress(start, end, 100) == 0.0
    assert transform.progress(start, end, 125) == 0.0625
    assert transform.progress(start, end, 150) == 0.25
    assert transform.progress(start, end, 200) == 1.0


def test_ease_out_curve():
    start = 100
    end = 200
    transform = EaseOutCurve()

    assert transform.progress(start, end, 100) == 0.0
    assert transform.progress(start, end, 125) == 0.4375
    assert transform.progress(start, end, 150) == 0.75
    assert transform.progress(start, end, 200) == 1.0


def test_ease_in_out_curve_combines_both_curves():
    start = 100
    end = 200
    transform = EaseInOutTransform()

    assert transform.progress(start, end, 100) == 0.0
    assert transform.progress(start, end, 125) == 0.125
    assert transform.progress(start, end, 150) == 0.5
    assert transform.progress(start, end, 175) == 0.875
    assert transform.progress(start, end, 200) == 1.0


def test_zero_endpoint_velocity_curve():
    start = 100
    end = 200
    transform = ZeroEndpointVelocityCurve()

    assert transform.progress(start, end, 100) == 0.0
    assert transform.progress(start, end, 125) == 0.15625
    assert transform.progress(start, end, 150) == 0.5
    assert transform.progress(start, end, 200) == 1.0


def test_zero_endpoint_acceleration_curve():
    start = 100
    end = 200
    transform = ZeroEndpointAccelerationCurve()

    assert transform.progress(start, end, 100) == 0.0
    assert transform.progress(start, end, 125) == 0.103515625
    assert transform.progress(start, end, 150) == 0.5
    assert transform.progress(start, end, 200) == 1.0


def test_instant_curve_always_returns_full_progress():
    transform = InstantCurve()
    start = 100
    end = 200

    assert transform.progress(start, end, 50) == 1.0
    assert transform.progress(start, end, 150) == 1.0
    assert transform.progress(start, end, 250) == 1.0
