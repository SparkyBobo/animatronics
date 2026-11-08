"""
DaBones

Processes messages for show.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.show.status import ShowStatusProcessor

from animacy.utils.logging import INFO, log

class ShowDispatcher:
    """Processes messages for show."""

    def __init__(self) -> None:
        """Initialize show processor."""
        log(5, INFO)
        self.handlers = []

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
        return result
    
