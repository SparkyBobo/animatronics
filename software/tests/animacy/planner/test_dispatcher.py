"""
Animacy

Planning dispatcher tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import PerformanceDataMessage
from animacy.planning.dispatcher import PlanningDispatcher
from unittest.mock import Mock

def test_dispatch_create():
    next_processor = Mock()
    disp = PlanningDispatcher(next=next_processor)
    assert disp
    assert disp.next == next_processor

def test_dispatch_subscribe():
    handler = Mock()
    disp = PlanningDispatcher(next=Mock())
    disp.subscribe(handler)
    assert handler in disp.handlers    

def test_dispatch_unsubscribe():
    handler = Mock()
    disp = PlanningDispatcher(next=Mock())
    disp.subscribe(handler)
    disp.unsubscribe(handler)
    assert not disp.handlers

def test_dispatch_process():
    next_processor = Mock()
    handler = Mock()
    disp = PlanningDispatcher(next=next_processor)
    disp.subscribe(handler)

    msg = PerformanceDataMessage()
    disp.process(msg)
    handler.process.assert_called_once_with(msg)
