"""
Animacy

Analog driver.

Copyright (c) 2026 Sparky Bobo
"""


from animacy.hardware.ports import IOPort



# An analog driver.
class AnalogDriver:
    """Analog driver."""

    def __init__(self, port: IOPort) -> None:
        """Initialize AnalogDriver."""
        self.port = port
