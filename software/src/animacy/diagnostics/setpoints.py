"""
Animacy

Setpoint diagnostics.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.setpoint import Setpoint

import logging
logger = logging.getLogger(__name__)

class SetpointDiagnostics:
    """Setpoint diagnostics."""

    def __init__(self, setpoints:list[Setpoint]) -> None:
        """Initialize SetpointDiagnostics."""
        self.setpoints = setpoints

    def is_enabled(self) -> bool:
        return len(self.setpoints) > 0

    def get_list(self) -> list[str]:
        return [setpoint.name for setpoint in self.setpoints]

    def select_index(self, index:int) -> Setpoint:
        return self.setpoints[index]

