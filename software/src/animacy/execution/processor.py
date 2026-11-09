"""
Animacy

Processes messages for execution.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import (
    PerformanceClockMessage,
    PerformanceLoadSongMessage,
    PerformanceMessage,
    PerformanceMessageProcessor,
    PerformanceMessageResult,
    PerformanceResetEventMessage,
    PerformanceSongPositionMessage,
    PerformanceSystemResetMessage,
)
from animacy.execution.executor import Executor
from animacy.utils.logging import INFO, log


class ExecutionProcessor:
    """Processes messages for execution."""

    def __init__(self, next: PerformanceMessageProcessor, executor: Executor) -> None:
        """Initialize execution processor."""
        log(5, INFO)
        self.next = next
        self.executor = executor

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        log(1, INFO, message.id, message.timecode)
        result = PerformanceMessageResult.SKIPPED
        if isinstance(
            message, (PerformanceSystemResetMessage, PerformanceResetEventMessage)
        ):
            self.executor.reset()
            result = PerformanceMessageResult.HANDLED

        if isinstance(message, PerformanceLoadSongMessage):
            self.executor.reset()
            result = PerformanceMessageResult.HANDLED

        if isinstance(message, PerformanceSongPositionMessage):
            self.executor.reset()
            result = PerformanceMessageResult.HANDLED

        if isinstance(message, PerformanceClockMessage):
            self.executor.evaluate()
            result = PerformanceMessageResult.HANDLED

        if self.executor.process(message) == PerformanceMessageResult.TERMINATE:
            return PerformanceMessageResult.TERMINATE

        if self.next:
            self.next.process(message)
        return result
