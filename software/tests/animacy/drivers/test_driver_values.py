"""
DaBones

Driver value tests.

Copyright (c) 2026 Sparky Bobo
"""

import pytest

from animacy.contracts.driver import (
    ColorDriverValue,
    DriverConstraints,
    IntensityDriverValue,
    PositionDriverValue,
)
from animacy.contracts.color import Color


def test_position_driver_value_interpolates_and_clamps_progress():
    start = PositionDriverValue(10)
    target = PositionDriverValue(30)

    assert start.interpolate(target, 0.5) == PositionDriverValue(20)
    assert start.interpolate(target, -1.0) == start
    assert start.interpolate(target, 2.0) == target


def test_intensity_driver_value_interpolates():
    start = IntensityDriverValue(0)
    target = IntensityDriverValue(200)

    assert start.interpolate(target, 0.25) == IntensityDriverValue(50)


def test_driver_value_interpolation_rejects_different_types():
    with pytest.raises(TypeError, match="same concrete type"):
        PositionDriverValue(10).interpolate(IntensityDriverValue(20), 0.5)


def test_color_driver_value_interpolates_each_channel():
    start = ColorDriverValue(Color(0, 10, 20, 30))
    target = ColorDriverValue(Color(100, 110, 120, 130))

    assert start.interpolate(target, 0.5) == ColorDriverValue(Color(50, 60, 70, 80))


def test_driver_constraints_include_value_bounds_and_motion_limits():
    bounded = DriverConstraints(
        minimum=PositionDriverValue(0),
        maximum=PositionDriverValue(100),
        max_velocity=12.5,
        max_acceleration=4.0,
    )
    unbounded = DriverConstraints()

    assert bounded.minimum == PositionDriverValue(0)
    assert bounded.maximum == PositionDriverValue(100)
    assert bounded.max_velocity == 12.5
    assert bounded.max_acceleration == 4.0
    assert unbounded.minimum is None
    assert unbounded.maximum is None
    assert unbounded.max_velocity is None
    assert unbounded.max_acceleration is None