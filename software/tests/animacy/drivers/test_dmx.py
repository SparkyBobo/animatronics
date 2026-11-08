"""
Animacy

DMX output driver tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.drivers.dmx import DMX_VALUES_INDEX0, DMXDriver


def test_dmx_driver_set_dmx_level():
    driver = DMXDriver()
    driver.set_dmx_level(1, 255)
    assert_transmitted_channel_value(driver, 1, 255)

def test_dmx_driver_get_dmx_level():
    driver = DMXDriver()
    driver.set_dmx_level(1, 255)
    assert driver.get_dmx_level(1) == 255

def test_dmx_driver_set_dmx_levels():
    driver = DMXDriver()
    driver.set_dmx_levels([
        (1, 255),
        (2, 128),
        (3, 64),
        (4, 0),
    ])
    assert_transmitted_channel_value(driver, 1, 255)
    assert_transmitted_channel_value(driver, 2, 128)
    assert_transmitted_channel_value(driver, 3, 64)
    assert_transmitted_channel_value(driver, 4, 0)

def test_dmx_driver_all_off():
    driver = DMXDriver()
    driver.set_dmx_levels([
        (1, 255),
        (2, 128),
        (3, 64),
    ])
    driver.all_off()
    assert_transmitted_channel_value(driver, 1, 0)
    assert_transmitted_channel_value(driver, 2, 0)
    assert_transmitted_channel_value(driver, 3, 0)

def test_dmx_driver_get_values():
    driver = DMXDriver()
    driver.set_dmx_levels([
        (1, 255),
        (2, 128),
        (3, 64),
    ])
    values = driver.get_values()
    assert len(values) == 512
    assert values[0] == 255
    assert values[1] == 128
    assert values[2] == 64

def test_dmx_driver_ignores_out_of_range_channels():
    driver = DMXDriver()
    driver.set_dmx_level(0, 255)
    driver.set_dmx_level(513, 255)
    driver.set_dmx_levels([(1, 200), (0, 255), (513, 255)])

    assert driver.get_dmx_level(0) == 0
    assert driver.get_dmx_level(1) == 200
    assert driver.get_dmx_level(513) == 0

def test_dmx_driver_clamps_channel_levels():
    driver = DMXDriver()
    driver.set_dmx_levels([(1, -1), (2, 256)])

    assert driver.get_dmx_level(1) == 0
    assert driver.get_dmx_level(2) == 255

def assert_transmitted_channel_value(driver, channel, value):
    assert driver.dmx_state_machine.last_write is not None
    assert driver.dmx_state_machine.last_write[DMX_VALUES_INDEX0 + channel - 1] == value
