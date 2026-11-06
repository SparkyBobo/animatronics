"""
DaBones

Processes messages for planning.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.contracts.planner import DriverValueCache

import logging
logger = logging.getLogger(__name__)

class PlanningProcessor:
    """Dispatch behaviors and record their planned driver values."""

    def __init__(
        self,
        next: PerformanceMessageProcessor,
        cache: DriverValueCache,
        handlers: list[PerformanceMessageProcessor] | None = None,
    ) -> None:
        """Initialize planning processor."""
        logger.info("Initialize PlanningProcessor.")
        self.next = next
        self.cache = cache
        self.handlers = handlers if handlers is not None else []

    def subscribe(self, handler: PerformanceMessageProcessor) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: PerformanceMessageProcessor) -> None:
        self.handlers.remove(handler)

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        logger.info(f"Process performance message {message.id}@{message.timecode}")
        result = PerformanceMessageResult.SKIPPED
        for handler in self.handlers:
            handler_result = handler.process(message)
            if handler_result == PerformanceMessageResult.TERMINATE:
                return handler_result
            if handler_result == PerformanceMessageResult.HANDLED:
                result = handler_result

        # Cache the updates and reschedule the message
        if isinstance(message, PerformanceDataMessage):
            for event in message.events:
                if event.transition is not None:
                    self.cache.update(event.transition, event.end)
                    result = PerformanceMessageResult.HANDLED

        if self.next:
            self.next.process(message)            
        return result
    
