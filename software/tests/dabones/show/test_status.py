"""
DaBones

Status tests.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.performance import *
from dabones.show.status import ShowStatusProcessor

def test_status_init():
    status = ShowStatusProcessor()
    assert not status.is_running
    assert status.show_clock == 0

def test_status_start():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.is_running
    assert status.show_clock == 0

def test_status_stop():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceSongStopMessage()) == PerformanceMessageResult.HANDLED
    assert not status.is_running
    assert status.show_clock == 0

def test_status_continue():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceSongStopMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceSongContinueMessage()) == PerformanceMessageResult.HANDLED
    assert status.is_running
    assert status.show_clock == 0

def test_status_update():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceClockMessage(timecode=42)) == PerformanceMessageResult.HANDLED
    assert status.is_running
    assert status.show_clock == 42

def test_status_load():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceClockMessage(timecode=42)) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceLoadSongMessage()) == PerformanceMessageResult.HANDLED
    assert not status.is_running
    assert status.show_clock == 0

def test_status_load():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceClockMessage(timecode=42)) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceSongPositionMessage(position=42)) == PerformanceMessageResult.HANDLED
    assert not status.is_running
    assert status.show_clock == 42

def test_status_system_reset():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceSystemResetMessage()) == PerformanceMessageResult.HANDLED
    assert not status.is_running
    assert status.show_clock == 0

def test_status_event_reset():
    status = ShowStatusProcessor()
    assert status.process(PerformanceSongStartMessage()) == PerformanceMessageResult.HANDLED
    assert status.process(PerformanceResetEventMessage()) == PerformanceMessageResult.HANDLED
    assert not status.is_running
    assert status.show_clock == 0

def test_status_skipped():
    status = ShowStatusProcessor()
    assert status.process(PerformanceFileCompleteMessage()) == PerformanceMessageResult.SKIPPED
    assert not status.is_running
    assert status.show_clock == 0
