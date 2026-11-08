"""
Animacy

Desktop shim for busio.

Copyright (c) 2026 Sparky Bobo
"""

from typing import Optional

class UART:
    """Digital IO Shim"""

    def __init__(self, tx, rx, baudrate, bits, parity, stop, timeout):
        self.tx = tx
        self.rx = rx
        self.baudrate = baudrate
        self.bits = bits
        self.parity = parity
        self.stop = stop
        self.timeout = timeout

    def read(self, size: Optional[int] = None) -> bytes:
        return None

    def readline(self) -> bytes:
        return None

    def write(self, data: bytes) -> None:
        return None

    def deinit(self) -> None:
        pass