"""
DaBones

SetpointDiagnostics test.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.setpoint import Setpoint
from animacy.diagnostics.setpoints import SetpointDiagnostics

def test_setpoint_dignostics_create():
    diag = SetpointDiagnostics([])
    assert diag.is_enabled() == False

def test_setpoint_dignostics_is_enable():
    setpoints = get_setpoint()
    diag = SetpointDiagnostics(setpoints)
    assert diag.is_enabled() == True

def test_setpoint_dignostics_get_named():
    setpoints = get_setpoint()
    diag = SetpointDiagnostics(setpoints)
    assert diag.get_list() == [setpoint.name for setpoint in setpoints]

def test_setpoint_dignostics_select():
    setpoints = get_setpoint()
    diag = SetpointDiagnostics(setpoints)
    selected = diag.select_index(0)
    assert selected.name == setpoints[0].name

def get_setpoint() -> list[Setpoint]:
    driver1 = Mock()
    driver2 = Mock()
    return [
        Setpoint("setpoint1", DriverTransition(driver1, PositionDriverValue(85), PositionDriverValue(85))),
        Setpoint("setpoint2", DriverTransition(driver1, PositionDriverValue(95), PositionDriverValue(95))),
        Setpoint("setpoint3", DriverTransition(driver2, PositionDriverValue(85), PositionDriverValue(85))),
        Setpoint("setpoint4", DriverTransition(driver2, PositionDriverValue(95), PositionDriverValue(95))),
    ]