"""
DaBones

Logging utilities.

Copyright (c) 2026 Sparky Bobo
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

LOG_LEVEL = 2

CRITICAL = ERROR = 1
WARNING = INFO = 2
DEBUG = 3

_module_path = __file__.replace("\\", "/")
_package_path = _module_path.rsplit("/", 2)[0] if "/" in _module_path else "."
_LOG_STRINGS_PATH = _package_path + "/log_strings.txt"


def log(message_id: int, severity: int, *args: object) -> None:
    """Print a catalog message when its severity is enabled."""
    if severity not in (CRITICAL, WARNING, DEBUG):
        raise ValueError(f"Invalid log severity: {severity}")
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

    print(template.format(*args))


class Logging:
    """Logging utilities."""

    def __init__(self) -> None:
        """Initialize Logging."""
        pass
