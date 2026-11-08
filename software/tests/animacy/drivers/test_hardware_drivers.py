"""
DaBones

Hardware driver tests.

Copyright (c) 2026 Sparky Bobo
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import pytest

from animacy.contracts.color import Color
from animacy.contracts.driver import (
    AddressableDriverTransition,
    ColorDriverValue,
    DriverTransition,
    IntensityDriverValue,
    PositionDriverValue,
)
from animacy.drivers.led import LedDriver
from animacy.drivers.servo import ServoDriver


def test_led_driver_writes_color_and_brightness(monkeypatch):
    pixels = MagicMock()
    monkeypatch.setattr("animacy.drivers.led.neopixel.NeoPixel", Mock(return_value=pixels))
    driver = LedDriver(count=4)

    driver.process(
        AddressableDriverTransition(
            driver=driver,
            start_value=ColorDriverValue(Color(0, 0, 0)),
            end_value=ColorDriverValue(Color(10, 20, 30)),
            progress=1,
            address=2,
        )
    )
    driver.process(
        DriverTransition(
            driver=driver,
            start_value=IntensityDriverValue(0),
            end_value=IntensityDriverValue(128),
            progress=1,
        )
    )

    assert driver.pixel_count == 4
    pixels.__setitem__.assert_called_once_with(2, (10, 20, 30))
    assert pixels.brightness == pytest.approx(128 / 255)
    assert pixels.show.call_count == 2


def test_led_driver_constraints_reject_unsupported_values(monkeypatch):
    monkeypatch.setattr("animacy.drivers.led.neopixel.NeoPixel", Mock())
    driver = LedDriver()

    assert driver.constraints_for(ColorDriverValue(Color())) == driver.color_constraints
    assert driver.constraints_for(IntensityDriverValue(10)) == driver.intensity_constraints
    with pytest.raises(ValueError, match="Unsupported driver value"):
        driver.constraints_for(PositionDriverValue(10))


def test_servo_driver_sets_pwm_duty_for_position(monkeypatch):
    pwm = Mock()
    monkeypatch.setattr("animacy.drivers.servo.PWMOut", Mock(return_value=pwm))
    driver = ServoDriver(SimpleNamespace(pin="servo-pin"))

    driver.process(
        DriverTransition(
            driver=driver,
            start_value=PositionDriverValue(800),
            end_value=PositionDriverValue(2000),
            progress=1,
        )
    )

    assert pwm.duty_cycle == int(2000 / 20000 * 65535)
    assert driver.constraints_for(PositionDriverValue(100)) == driver.constraints
    with pytest.raises(ValueError, match="Unsupported driver value"):
        driver.constraints_for(IntensityDriverValue(10))
