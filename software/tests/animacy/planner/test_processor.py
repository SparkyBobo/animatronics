"""
Animacy

Planning processor tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.performance import *
from animacy.planning.cache import PlanningCache
from animacy.planning.processor import PlanningProcessor


def test_processor_init():
    next_processor = Mock()
    cache = PlanningCache()
    processor = PlanningProcessor(next=next_processor, cache=cache)
    assert processor.next == next_processor
    assert processor.cache is cache

def test_processor_process():
    next_processor = Mock()
    cache = Mock(wraps=PlanningCache())
    value = PositionDriverValue(42)
    transition = DriverTransition(Mock(), value, value)
    behavior = Mock()

    def append_transition(message):
        message.events.append(
            PerformanceEvent(transition=transition, end=10)
        )
        return PerformanceMessageResult.HANDLED

    behavior.process.side_effect = append_transition
    processor = PlanningProcessor(next=next_processor, cache=cache, handlers=[behavior])
    message = PerformanceDataMessage(timecode=10, events=[])

    assert processor.process(message) == PerformanceMessageResult.HANDLED
    behavior.process.assert_called_once_with(message)
    cache.update.assert_called_once_with(transition, 10)
    next_processor.process.assert_called_once_with(message)

def test_processor_does_not_dispatch_terminated_messages():
    next_processor = Mock()
    handler = Mock()
    handler.process.return_value = PerformanceMessageResult.TERMINATE
    processor = PlanningProcessor(
        next=next_processor,
        cache=PlanningCache(),
        handlers=[handler],
    )
    message = PerformanceDataMessage()

    assert processor.process(message) == PerformanceMessageResult.TERMINATE

    next_processor.process.assert_not_called()

def test_processor_subscribe_and_unsubscribe_handlers():
    processor = PlanningProcessor(next=Mock(), cache=PlanningCache())
    handler = Mock()

    processor.subscribe(handler)
    processor.subscribe(handler)
    assert processor.handlers == [handler]

    processor.unsubscribe(handler)
    assert processor.handlers == []
