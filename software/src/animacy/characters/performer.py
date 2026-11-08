"""
Animacy

Foundational performer.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import MidiMessage, MidiChannelMessage, MidiMessageProcessor, MidiMessageResult

from animacy.utils.logging import INFO, log

class PerformerBase(MidiMessageProcessor):
    """Base character."""

    def __init__(self, name: str, channel:int) -> None:
        """Initialize Character.

        Args:
            name: character name.
            midi_channel: MIDI channel number (1-16, 1-based).
        """
        log(5, INFO)
        self.name = name
        self.channel = channel - 1
        pass

    def map(self, timecode: int, message:MidiMessage) -> MidiMessageResult:
        # Allow data through
        if (not isinstance(message, MidiChannelMessage)):
            return MidiMessageResult.HANDLED
        # Allow my channels through
        if (message.channel == self.channel):
            return MidiMessageResult.HANDLED
        # Allow global channels through
        if (message.channel == 15):
            return MidiMessageResult.HANDLED
        # block all others
        return MidiMessageResult.TERMINATE

