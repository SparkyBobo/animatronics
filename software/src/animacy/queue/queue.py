"""
Animacy

Queue for PerformanceMessage items.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import PerformanceMessage
from animacy.utils.counter import Counter
import gc

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
        self.sequence = Counter()

    def queue(self, message:PerformanceMessage) -> None:
        """Queue a message."""
        #self._insort(self.messages, (message.timecode, next(self.sequence), message))
        gc.collect()
        self.messages.append(message)

    def peek(self) -> PerformanceMessage | None:
        """Peek at the next message in the queue."""
        if self.messages:
            #_, _, message = self.messages[0]
            message = self.messages[0]
            return message
        return None

    def dequeue(self) -> PerformanceMessage | None:
        """Dequeue the next message in the queue."""
        if self.messages:
            #_, _, message = self.messages.pop(0)
            message = self.messages.pop(0)
            return message
        return None

    @staticmethod
    def _insort(a, x):
        lo = 0
        hi = len(a)

        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1

        a.insert(lo, x)
