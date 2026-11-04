"""
DaBones

Dispatches messages to performance processors.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.performance import *

import logging
logger = logging.getLogger(__name__)

class PlanningDispatcher:
    """Processes the performance control messages."""

    def __init__(self, next: PerformanceMessageProcessor, handlers: PerformanceMessageProcessor = None) -> None:
        """Initialize PerformanceMessageDispatcher."""
        self.next = next
        self.handlers = handlers if handlers is not None else []

    def subscribe(self, handler: PerformanceMessageProcessor):
        """Subscribe a PerformanceMessageProcessor."""
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: PerformanceMessageProcessor):
        """Unsubscribe a PerformanceMessageProcessor: handler."""
        self.handlers.remove(handler)      

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        """Dispatch message to all subscribers."""
        for handler in self.handlers:
            result = handler.process(message)
            if result == PerformanceMessageResult.TERMINATE:
                return result
        if self.next:
            return self.next.process(message)