"""
Animacy

Dispatches MIDI messages.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import MidiMessage, MidiMessageResult, MidiMessageProcessor

import logging
logger = logging.getLogger(__name__)

class MidiMessageDispatcher:
    """Dispatches the midi messages."""

    def __init__(self, handlers: list[MidiMessageProcessor] = None) -> None:
        """Initialize MidiMessageDispatcher."""
        self.handlers = handlers or []

    def subscribe(self, handler: MidiMessageProcessor):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: MidiMessageProcessor):
        self.handlers.remove(handler)

    def map(self, timecode: int, message:MidiMessage) -> MidiMessageResult:
        result = MidiMessageResult.SKIPPED
        for handler in self.handlers:
            handler_result = handler.map(timecode, message)
            if (handler_result == MidiMessageResult.TERMINATE):
                # We never propogate the result, it's terminated after dispatch.
                return MidiMessageResult.TERMINATE
            if (handler_result == MidiMessageResult.HANDLED):
                # We never propogate the result, it's terminated after dispatch.
                result = MidiMessageResult.HANDLED
        return result
