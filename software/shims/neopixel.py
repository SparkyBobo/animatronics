"""
Animacy

Desktop shim for neopixel.

Copyright (c) 2026 Sparky Bobo
"""

class NeoPixel:
    """NeoPixel Shim"""

    def __init__(self, pin, n) -> None:
        self.pin = pin
        self.count = n

    def show(self) -> None:
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def deinit(self) -> None:
        pass