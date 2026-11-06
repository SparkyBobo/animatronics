"""
DaBones

Setpoint contract.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.driver import DriverValue

# A named driver value representing important keyframes within a driver or behaviour.
class Setpoint:
    """
    Represents a named/fixed driver value.

    Attributes:
        name: The name of the setpoint.
        transition: The driver transition for the setpoint.
    """
    
    def __init__(self, name: str = None, value: DriverValue = None):
        super().__init__()
        self.name = name
        self.value = value    
