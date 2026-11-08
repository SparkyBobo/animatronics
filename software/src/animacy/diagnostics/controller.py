"""
DaBones

Interfaces with diagnostics controller.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import PerformanceMessageProcessor

import logging
logger = logging.getLogger(__name__)

class DiagnosticController:
    """Interfaces with diagnostics controller."""

    def __init__(self, processor: PerformanceMessageProcessor) -> None:
        """Initialize DiagnosticController."""
        self.processor = processor

