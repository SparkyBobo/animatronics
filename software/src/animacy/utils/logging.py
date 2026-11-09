"""
Animacy

Logging utilities.

Copyright (c) 2026 Sparky Bobo
"""

from __future__ import annotations

import logging

LOG_LEVEL = 2
MEMORY_LOGGING = True

CRITICAL = ERROR = 1
WARNING = INFO = 2
DEBUG = 3
MEMORY = 4

_module_path = __file__.replace("\\", "/")
_package_path = _module_path.rsplit("/", 2)[0] if "/" in _module_path else "."
_LOG_STRINGS_PATH = _package_path + "/log_strings.txt"


class CatalogLogger:
    """Resolve integer message IDs and emit them through a standard logger."""

    def __init__(self, name: str) -> None:
        self.source = logging.getLogger(name)

    def log(self, message_id: int, severity: int, *args: object) -> None:
        """Log a catalog message when its severity is enabled."""
        if severity not in (CRITICAL, WARNING, DEBUG, MEMORY):
            raise ValueError(f"Invalid log severity: {severity}")
        if severity == MEMORY:
            if not MEMORY_LOGGING:
                return
        else:
            if LOG_LEVEL not in (0, CRITICAL, WARNING, DEBUG):
                raise ValueError(f"Invalid log level: {LOG_LEVEL}")
            if LOG_LEVEL == 0 or severity > LOG_LEVEL:
                return

        template = None
        with open(_LOG_STRINGS_PATH, "r") as catalog:
            for line_number, line in enumerate(catalog, start=1):
                record = line.rstrip("\r\n")
                if not record.strip() or record.lstrip().startswith("#"):
                    continue

                id_text, separator, message = record.partition("|")
                if not separator:
                    raise ValueError(
                        f"Malformed log catalog entry on line {line_number}"
                    )
                try:
                    current_id = int(id_text)
                except ValueError as error:
                    raise ValueError(
                        f"Invalid log catalog ID on line {line_number}: {id_text!r}"
                    ) from error

                if current_id == message_id:
                    template = message
                    break

        if template is None:
            raise KeyError(f"Log message ID not found: {message_id}")

        level = {
            CRITICAL: logging.ERROR,
            WARNING: logging.INFO,
            DEBUG: logging.DEBUG,
            MEMORY: logging.INFO,
        }[severity]
        self.source.log(level, template.format(*args))
