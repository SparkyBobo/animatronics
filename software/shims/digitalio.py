"""
Animacy

Desktop shim for digitalio.

Copyright (c) 2026 Sparky Bobo
"""

class Direction:
    OUTPUT = "output"
    INPUT = "input"

class DigitalInOut:
    """Digital IO Shim"""

    def __init__(self, pin) -> None:
        self.pin = pin
        self.value = False
        self.direction = None

    def switch_to_output(self, value=False) -> None:
        self.value = value

    def switch_to_input(self) -> None:
        pass

    def deinit(self) -> None:
        pass