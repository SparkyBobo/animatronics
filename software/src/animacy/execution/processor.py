"""
DaBones

Processes messages for execution.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import *
from animacy.execution.executor import Executor

import logging
logger = logging.getLogger(__name__)

class ExecutionProcessor:
    """Processes messages for execution."""

    def __init__(self, next: PerformanceMessageProcessor, executor: Executor) -> None:
        """Initialize execution processor."""
        logger.info("Initialize ExecutionProcessor.")
        self.next = next
        self.executor = executor

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        logger.info(f"Process performance message {message.id}@{message.timecode}")
        result = PerformanceMessageResult.SKIPPED
        if (isinstance(message, PerformanceSystemResetMessage) or isinstance(message, PerformanceResetEventMessage)):
            self.executor.reset()
            result = PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceLoadSongMessage)):
            self.executor.reset()
            result = PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceSongPositionMessage)):
            self.executor.reset()
            result = PerformanceMessageResult.HANDLED

        if (isinstance(message, PerformanceClockMessage)):
            self.executor.evaluate()
            result = PerformanceMessageResult.HANDLED
        
        if (self.executor.process(message) == PerformanceMessageResult.TERMINATE):
            return PerformanceMessageResult.TERMINATE
    
        if self.next:
            self.next.process(message)            
        return result
    
