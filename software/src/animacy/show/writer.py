"""
DaBones

Show writer.

Copyright (c) 2026 Sparky Bobo
"""

import os
import tempfile

from animacy.contracts.performance import (
    PerformanceControlMessage,
    PerformanceFileCompleteMessage,
    PerformanceFileContentMessage,
    PerformanceFileHeaderMessage,
    PerformanceMessageResult,
)
from animacy.utils.logging import ERROR, log


class ShowWriter:
    """Show file writer."""

    def __init__(self) -> None:
        """Initialize ShowFileWriter."""
        self.file = None
        self.tempname = None
        self.checksum = 0
        self.sequence = 0
        self.filename = None

    def process(self, event:PerformanceControlMessage) -> PerformanceMessageResult:
        if isinstance(event, PerformanceFileHeaderMessage):
            return PerformanceMessageResult.HANDLED_CONTINUE if self.open(event.name) else PerformanceMessageResult.NOT_HANDLED
        if isinstance(event, PerformanceFileContentMessage):
            return PerformanceMessageResult.HANDLED_CONTINUE if self.write(event.sequence, event.data) else PerformanceMessageResult.NOT_HANDLED
        if isinstance(event, PerformanceFileCompleteMessage):
            return PerformanceMessageResult.HANDLED_CONTINUE if self.close(event.checksum) else PerformanceMessageResult.NOT_HANDLED

    def open(self, name: str) -> bool:
        try:
            # Open a temp file
            fd, path = tempfile.mkstemp(suffix=".tmp")
            self.tempname = path
            self.file = os.fdopen(fd, "wb")
            # Track the filename and reset the checksum
            self.checksum = 0
            self.sequence = 0
            self.filename = name
            return True
        except OSError as ex:
            log(1716, ERROR, self.tempname, ex)
            if (self.file):
                self.file.close()
                self.file = None
            return False

    def write(self, sequence: int, data: bytes) -> bool:
        # verify sequence
        self.sequence += 1
        if (self.sequence != sequence):
            log(1717, ERROR, self.sequence, sequence)
            return False
        # write to the temp file
        if (self.file):
            self.file.write(data)
            self.checksum = sum(data) & 0xFFFF
            return True
        return False

    def close(self, checksum: int) -> bool:
        # cluse the temp file and close it
        self.file.flush()
        self.file.close()
        # verify checksum
        if (self.checksum != checksum):
            log(1718, ERROR, self.checksum, checksum)
            return False
        # rename file
        os.rename(self.tempname, self.filename)
        return True
