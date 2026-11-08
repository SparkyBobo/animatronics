"""
DaBones

Processes messages against the show clock.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.contracts.queue import QueuePolicy
from animacy.queue.queue import PerformanceMessageQueue

from animacy.utils.logging import INFO, log

class QueueProcessor:
    """Processes messages against the show clock."""

    def __init__(self, next: PerformanceMessageProcessor, policy: QueuePolicy) -> None:
        """Initialize queue processor."""
        log(5, INFO)
        self.next = next
        self.policy = policy
        self.queue = PerformanceMessageQueue()

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        result = self._process(message)
        if result == PerformanceMessageResult.TERMINATE or result == PerformanceMessageResult.QUEUED:
            return result

        if self.next:
            self.next.process(message)
        return result

    def _process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        log(1, INFO, message.id, message.timecode)
        if (isinstance(message, PerformanceSystemResetMessage) or isinstance(message, PerformanceResetEventMessage)):
            self.queue.reset()
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceLoadSongMessage)):
            self.queue.reset()
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongStartMessage) or isinstance(message, PerformanceClockMessage)):
            dequeued_messages = self._dequeue()
            for msg in dequeued_messages:
                self.next.process(msg)
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongPositionMessage)):
            _ = self._dequeue()
            return PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceMessage)):
            outcome = self.policy.process(message)
            if (outcome == PerformanceMessageResult.QUEUED):
                self.queue.queue(message)
            return outcome

    def _dequeue(self) -> list[PerformanceMessage]:
        dequeued_messages = []
        next_message = self.queue.peek()
        while next_message:
            outcome = self.policy.process(next_message)
            if (outcome == PerformanceMessageResult.QUEUED):
                break
            
            dequeued_messages.append(self.queue.dequeue())
            next_message = self.queue.peek()
        return dequeued_messages
    
