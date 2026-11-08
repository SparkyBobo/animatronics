"""
DaBones

Audio driver tests.

Copyright (c) 2026 Sparky Bobo
"""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from animacy.contracts.driver import (
    AudioDriverValue,
    DriverTransition,
    IntensityDriverValue,
)
from animacy.contracts.service import ServiceResult
from animacy.drivers.audio import AudioDriver


@pytest.fixture
def driver(monkeypatch):
    uart = Mock()
    monkeypatch.setattr("animacy.drivers.audio.busio.UART", Mock(return_value=uart))
    port = SimpleNamespace(txpin="tx", rxpin="rx", baudrate=115200, timeout=0.02)
    instance = AudioDriver(port)
    return instance, uart


def test_audio_driver_sends_command(driver):
    instance, uart = driver

    instance.process(
        DriverTransition(
            driver=instance,
            start_value=AudioDriverValue("OLD"),
            end_value=AudioDriverValue("PLAY"),
        )
    )

    uart.write.assert_called_once_with(b"PLAY\r\n")


def test_audio_driver_constraints_only_accept_audio_values(driver):
    instance, _ = driver

    assert instance.constraints_for(AudioDriverValue("PLAY")) == instance.constraints
    with pytest.raises(ValueError, match="Unsupported driver value"):
        instance.constraints_for(IntensityDriverValue(5))


def test_audio_driver_service_reports_output_and_idle(driver):
    instance, uart = driver
    uart.readline.side_effect = [b"ready\r\n", b""]

    assert instance.service() == ServiceResult.ACTIVITY
    assert instance.service() == ServiceResult.IDLE


def test_audio_driver_pings_after_inactivity(driver, monkeypatch):
    instance, uart = driver
    instance.last_activity = 0
    monkeypatch.setattr("animacy.drivers.audio.time.monotonic", Mock(return_value=10))
    uart.readline.return_value = b""

    assert instance.service() == ServiceResult.IDLE

    uart.write.assert_called_once_with(b"PING\r\n")
    assert instance.last_activity == 10


def test_audio_driver_surfaces_non_ascii_output(driver):
    instance, uart = driver
    uart.readline.return_value = b"\xff"

    with pytest.raises(UnicodeDecodeError):
        instance.service()
