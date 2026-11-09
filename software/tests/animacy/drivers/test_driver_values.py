"""
Animacy

Driver value tests.

Copyright (c) 2026 Sparky Bobo
"""

import pytest

from animacy.contracts.color import Color
from animacy.contracts.driver import (
    AddressableDriverTransition,
    AudioDriverValue,
    ColorDriverValue,
    DriverConstraints,
    DriverTransition,
    IntensityDriverValue,
    PositionDriverValue,
)


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


@pytest.mark.parametrize(
    ("value_type", "components", "expected"),
    [
        (PositionDriverValue, (42,), PositionDriverValue(42)),
        (IntensityDriverValue, (128,), IntensityDriverValue(128)),
        (ColorDriverValue, (1, 2, 3, 4), ColorDriverValue(Color(1, 2, 3, 4))),
        (AudioDriverValue, (0,), AudioDriverValue("")),
    ],
)
def test_driver_values_round_trip_components(value_type, components, expected):
    assert value_type.from_components(components) == expected


@pytest.mark.parametrize(
    ("value_type", "components", "message"),
    [
        (PositionDriverValue, (), "one component"),
        (IntensityDriverValue, (1, 2), "one component"),
        (ColorDriverValue, (1, 2, 3), "four components"),
        (AudioDriverValue, (), "one component"),
    ],
)
def test_driver_values_reject_wrong_component_count(value_type, components, message):
    with pytest.raises(ValueError, match=message):
        value_type.from_components(components)


def test_audio_driver_value_is_a_discrete_transition():
    current = AudioDriverValue("stop")
    target = AudioDriverValue("play")

    assert current.components() == (0,)
    assert current.interpolate(target, 0.0) is target


def test_driver_transition_requires_matching_value_types():
    with pytest.raises(TypeError, match="same concrete type"):
        DriverTransition(
            driver=object(),
            start_value=PositionDriverValue(0),
            end_value=IntensityDriverValue(1),
        )


def test_driver_transition_keys_include_driver_and_address():
    driver = object()
    start = PositionDriverValue(0)
    end = PositionDriverValue(10)
    transition = DriverTransition(driver, start, end)
    addressed = AddressableDriverTransition(driver, start, end, address=3)

    assert transition.key == f"{id(driver)}:PositionDriverValue"
    assert transition.id == f"{transition.key}:{start}:{end}"
    assert addressed.key == f"{id(driver)}:3:PositionDriverValue"
