"""
Animacy

Queue for PerformanceMessage items.

Copyright (c) 2026 Sparky Bobo
"""

from __future__ import annotations

import gc

from animacy.contracts.performance import PerformanceMessage
from animacy.utils.logging import INFO, log


class PerformanceMessageQueue:
    """Queues commands against the show clock."""

    def __init__(self) -> None:
        """Initialize message queue."""
        log(5, INFO)
        self.next = next
        self.reset()

    def reset(self) -> None:
        """Reset the message queue and clear the event queue."""
        log(1606, INFO)
        self.messages = []

    def queue(self, message:PerformanceMessage) -> None:
        """Queue a message."""
        gc.collect()
        self.messages.append(message)

    def peek(self) -> PerformanceMessage | None:
        """Peek at the next message in the queue."""
        if self.messages:
            message = self.messages[0]
            return message
        return None

    def dequeue(self) -> PerformanceMessage | None:
        """Dequeue the next message in the queue."""
        if self.messages:
            message = self.messages.pop(0)
            return message
        return None
