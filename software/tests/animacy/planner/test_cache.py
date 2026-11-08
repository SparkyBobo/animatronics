"""
DaBones

PlanningCache tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock
from animacy.contracts.driver import (
    AddressableDriverTransition,
    DriverTransition,
    IntensityDriverValue,
    PositionDriverValue,
)
from animacy.planning.cache import PlanningCache


_DRIVER = Mock()


def make_transition(value: int = 0, driver=_DRIVER) -> DriverTransition:
    """Create a position transition for testing."""
    endpoint = PositionDriverValue(value)
    return DriverTransition(driver=driver, start_value=endpoint, end_value=endpoint)


def test_get_missing_value():
    cache = PlanningCache()
    transition = make_transition()

    cached_value, cached_timecode = cache.get(transition)

    assert cached_value is None
    assert cached_timecode == 0


def test_update_and_get():
    cache = PlanningCache()
    transition = make_transition(value=100)
    timecode = 100

    cache.update(transition, timecode)

    cached_value, cached_timecode = cache.get(transition)

    assert cached_value == transition.end_value
    assert cached_timecode == timecode


def test_update_newer_event():
    cache = PlanningCache()
    first = make_transition(value=100)
    second = make_transition(value=200)

    cache.update(first, 100)
    cache.update(second, 200)

    cached_value, cached_timecode = cache.get(second)

    assert cached_value == second.end_value
    assert cached_timecode == 200


def test_ignore_older_event():
    cache = PlanningCache()
    newer = make_transition(value=200)
    older = make_transition(value=100)

    cache.update(newer, 200)
    cache.update(older, 100)

    cached_value, cached_timecode = cache.get(newer)

    assert cached_value == newer.end_value
    assert cached_timecode == 200


def test_equal_timecode_is_ignored():
    cache = PlanningCache()
    first = make_transition(value=100)
    second = make_transition(value=200)

    cache.update(first, 100)
    cache.update(second, 100)

    cached_value, cached_timecode = cache.get(second)

    assert cached_value == first.end_value
    assert cached_timecode == 100


def test_different_keys_are_independent():
    cache = PlanningCache()
    driver = Mock()
    head = make_transition(driver=driver, value=100)
    foot_value = IntensityDriverValue(200)
    foot = DriverTransition(driver, foot_value, foot_value)

    cache.update(head, 100)
    cache.update(foot, 200)

    cached_head, head_timecode = cache.get(head)
    cached_foot, foot_timecode = cache.get(foot)

    assert cached_head == head.end_value
    assert head_timecode == 100

    assert cached_foot == foot.end_value
    assert foot_timecode == 200


def test_addressable_commands_have_independent_cache_entries():
    cache = PlanningCache()
    driver = Mock()
    first_value = PositionDriverValue(10)
    second_value = PositionDriverValue(20)
    first = AddressableDriverTransition(driver, first_value, first_value, address=1)
    second = AddressableDriverTransition(driver, second_value, second_value, address=2)

    cache.update(first, 100)
    cache.update(second, 200)

    assert cache.get(first) == (first.end_value, 100)
    assert cache.get(second) == (second.end_value, 200)