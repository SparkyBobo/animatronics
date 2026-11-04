"""
DaBones

On/off driver.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.hardware.ports import IOPort

import logging
logger = logging.getLogger(__name__)

# An digitial IO (on/off) driver.
class OnOffDriver:
    """On/off driver."""

    def __init__(self, port:IOPort) -> None:
        """Initialize OnOffDriver."""
        self.port = port
        pass

