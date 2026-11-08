"""
Animacy

USB Host for MIDI messages.

Copyright (c) 2026 Sparky Bobo
"""

import logging
logger = logging.getLogger(__name__)

class MidiUsbHost:
    """Reads/Writes MIDI messages from USB host."""

    def __init__(self) -> None:
        """Initialize MidiUsbHost."""
        pass

    @property
    def device(self) -> any:
        return None
