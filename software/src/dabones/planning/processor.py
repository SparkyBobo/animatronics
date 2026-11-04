"""
DaBones

Processes messages for planning.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.contracts.performance
import dabones.contracts.planner

import logging
logger = logging.getLogger(__name__)

class PlanningProcessor:
    """Dispatch behaviors and record their planned driver values."""

    def __init__(
        self,
        next: dabones.contracts.performance.PerformanceMessageProcessor,
        cache: dabones.contracts.planner.DriverValueCache,
        handlers: list[dabones.contracts.performance.PerformanceMessageProcessor] | None = None,
    ) -> None:
        """Initialize planning processor."""
        logger.info("Initialize PlanningProcessor.")
        self.next = next
        self.cache = cache
        self.handlers = handlers if handlers is not None else []

    def subscribe(self, handler: dabones.contracts.performance.PerformanceMessageProcessor) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: dabones.contracts.performance.PerformanceMessageProcessor) -> None:
        self.handlers.remove(handler)

    def process(self, message: dabones.contracts.performance.PerformanceMessage) -> dabones.contracts.performance.PerformanceMessageResult:
        logger.info(f"Process performance message {message.id}@{message.timecode}")
        result = dabones.contracts.performance.PerformanceMessageResult.SKIPPED
        for handler in self.handlers:
            handler_result = handler.process(message)
            if handler_result == dabones.contracts.performance.PerformanceMessageResult.TERMINATE:
                return handler_result
            if handler_result == dabones.contracts.performance.PerformanceMessageResult.HANDLED:
                result = handler_result

        if isinstance(message, dabones.contracts.performance.PerformanceDataMessage):
            for event in message.events:
                if event.transition is not None:
                    self.cache.update(event.transition, event.end)
                    result = dabones.contracts.performance.PerformanceMessageResult.HANDLED

        if self.next:
            self.next.process(message)
        return result
