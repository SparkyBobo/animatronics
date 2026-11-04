"""
DaBones

Dispatches messages to performance processors.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.contracts.performance

import logging
logger = logging.getLogger(__name__)

class PlanningDispatcher:
    """Processes the performance control messages."""

    def __init__(self, next: dabones.contracts.performance.PerformanceMessageProcessor, handlers: dabones.contracts.performance.PerformanceMessageProcessor = None) -> None:
        """Initialize PerformanceMessageDispatcher."""
        self.next = next
        self.handlers = handlers if handlers is not None else []

    def subscribe(self, handler: dabones.contracts.performance.PerformanceMessageProcessor):
        """Subscribe a PerformanceMessageProcessor."""
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: dabones.contracts.performance.PerformanceMessageProcessor):
        """Unsubscribe a PerformanceMessageProcessor: handler."""
        self.handlers.remove(handler)

    def process(self, message: dabones.contracts.performance.PerformanceMessage) -> dabones.contracts.performance.PerformanceMessageResult:
        """Dispatch message to all subscribers."""
        for handler in self.handlers:
            result = handler.process(message)
            if result == dabones.contracts.performance.PerformanceMessageResult.TERMINATE:
                return result
        if self.next:
            return self.next.process(message)
