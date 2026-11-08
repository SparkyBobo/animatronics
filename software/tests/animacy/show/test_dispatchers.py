"""
DaBones

Message dispatcher tests.

Copyright (c) 2026 Sparky Bobo
"""

from unittest.mock import Mock

from animacy.contracts.midi import MidiMessageResult
from animacy.contracts.performance import PerformanceMessageResult
from animacy.midi.dispatcher import MidiMessageDispatcher
from animacy.planning.dispatcher import PlanningDispatcher
from animacy.show.dispatcher import ShowDispatcher


def test_midi_dispatcher_tracks_handled_result_and_stops_on_terminate():
    skipped = Mock(map=Mock(return_value=MidiMessageResult.SKIPPED))
    handled = Mock(map=Mock(return_value=MidiMessageResult.HANDLED))
    terminating = Mock(map=Mock(return_value=MidiMessageResult.TERMINATE))
    after_terminate = Mock()
    dispatcher = MidiMessageDispatcher([skipped, handled, terminating, after_terminate])

    assert dispatcher.map(3, object()) == MidiMessageResult.TERMINATE

    skipped.map.assert_called_once()
    handled.map.assert_called_once()
    terminating.map.assert_called_once()
    after_terminate.map.assert_not_called()


def test_midi_dispatcher_subscription_is_unique_and_removable():
    dispatcher = MidiMessageDispatcher()
    handler = Mock()

    dispatcher.subscribe(handler)
    dispatcher.subscribe(handler)
    assert dispatcher.handlers == [handler]

    dispatcher.unsubscribe(handler)

    assert dispatcher.handlers == []
    assert dispatcher.map(0, object()) == MidiMessageResult.SKIPPED


def test_planning_dispatcher_stops_when_handler_terminates():
    handler = Mock(process=Mock(return_value=PerformanceMessageResult.TERMINATE))
    downstream = Mock()
    dispatcher = PlanningDispatcher(next=downstream, handlers=[handler])
    message = object()

    assert dispatcher.process(message) == PerformanceMessageResult.TERMINATE

    handler.process.assert_called_once_with(message)
    downstream.process.assert_not_called()


def test_planning_dispatcher_forwards_when_handlers_continue():
    handler = Mock(process=Mock(return_value=PerformanceMessageResult.SKIPPED))
    downstream = Mock(process=Mock(return_value=PerformanceMessageResult.HANDLED))
    dispatcher = PlanningDispatcher(next=downstream, handlers=[handler])
    message = object()

    assert dispatcher.process(message) == PerformanceMessageResult.HANDLED

    downstream.process.assert_called_once_with(message)


def test_planning_dispatcher_without_downstream_returns_none():
    dispatcher = PlanningDispatcher(next=None)

    assert dispatcher.process(object()) is None


def test_show_dispatcher_handles_empty_and_subscribed_cases():
    dispatcher = ShowDispatcher()
    message = object()

    assert dispatcher.process(message) == PerformanceMessageResult.SKIPPED

    handler = Mock(process=Mock(return_value=PerformanceMessageResult.HANDLED))
    dispatcher.subscribe(handler)
    dispatcher.subscribe(handler)
    assert dispatcher.handlers == [handler]
    assert dispatcher.process(message) == PerformanceMessageResult.HANDLED

    dispatcher.unsubscribe(handler)
    assert dispatcher.handlers == []
