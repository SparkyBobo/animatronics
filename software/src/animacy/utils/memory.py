"""Heap memory measurements for constrained runtimes."""

from __future__ import annotations

import gc

from animacy.utils import logging as logging_utils
from animacy.utils.logging import MEMORY, CatalogLogger

AFTER_SHOW_READER_INIT = 900
BEFORE_MIDI_LOAD = 901
AFTER_MIDI_LOAD = 902
QUEUE_COLLECT = 903


class MemoryMonitor:
    """Record heap measurements through the tokenized logging catalog."""

    def __init__(self) -> None:
        self.logger = CatalogLogger("animacy.memory")

    def collect(self, checkpoint_id: int) -> None:
        """Collect garbage and log before and after heap use in one record."""
        if not logging_utils.MEMORY_LOGGING:
            gc.collect()
            return

        mem_alloc = getattr(gc, "mem_alloc", None)
        mem_free = getattr(gc, "mem_free", None)
        if not callable(mem_alloc) or not callable(mem_free):
            gc.collect()
            return

        before_alloc = mem_alloc()
        before_free = mem_free()
        gc.collect()
        after_alloc = mem_alloc()
        after_free = mem_free()
        self.logger.log(
            checkpoint_id,
            MEMORY,
            before_alloc,
            before_free,
            after_alloc,
            after_free,
        )

    def record(self, checkpoint_id: int) -> None:
        """Log allocated and free heap bytes for a catalog checkpoint."""
        if not logging_utils.MEMORY_LOGGING:
            return

        mem_alloc = getattr(gc, "mem_alloc", None)
        mem_free = getattr(gc, "mem_free", None)
        if not callable(mem_alloc) or not callable(mem_free):
            return

        self.logger.log(checkpoint_id, MEMORY, mem_alloc(), mem_free())
