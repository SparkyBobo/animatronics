"""
Animacy

Linear buffer.

Copyright (c) 2026 Sparky Bobo
"""

import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)


class LinearBufferReader:
    def peek(self, index: int = 0, count: int = 1) -> memoryview:
        pass

    def available(self, count: int) -> int:
        pass


class LinearBufferWriter:
    def consume(self, count: int) -> None:
        pass

    def append(self, data: Sequence[int]) -> None:
        pass

    def reset(self) -> None:
        pass


class LinearBuffer:
    """Linear Buffer."""

    MAX_BUFFER: int = 1024

    def __init__(self) -> None:
        """Initialize Linear Buffer."""
        self.buffer = bytearray(self.MAX_BUFFER)
        self.head = 0
        self.tail = 0

    def peek(self, index: int = 0, count: int = 1) -> memoryview:
        if self.head == self.tail:
            return None
        end = min(index + self.head + count, self.tail)
        return memoryview(self.buffer[index + self.head : end])

    def available(self) -> int:
        if self.head == self.tail:
            return 0
        return self.tail - self.head

    def consume(self, count: int) -> None:
        self.head = min(self.head + count, self.tail)
        if self.head == self.tail:
            self.head = 0
            self.tail = 0

    def append(self, data: Sequence[int]) -> None:
        if self.tail + len(data) > self.MAX_BUFFER:
            raise RuntimeError(f" LinearBuffer overrun: {self.tail + len(data)}")

        self.buffer[self.tail : self.tail] = data
        self.tail += len(data)

    def reset(self) -> None:
        self.head = 0
        self.tail = 0
