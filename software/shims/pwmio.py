"""
Animacy

Desktop shim for pwmio.

Copyright (c) 2026 Sparky Bobo
"""

class PWMOut:
    """PWMOut Shim"""

    def __init__(self, pin, frequency) -> None:
        self.pin = pin
        self.frequency = frequency
        self._duty_cycle = 0

    @property
    def duty_cycle (self) -> float:
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, val: int) -> None:
        self._duty_cycle = val
