#!/usr/bin/env python3
"""
Animacy

Audio service for pi zero.

Copyright (c) 2026 Sparky Bobo
"""

import logging
import os
import signal
import subprocess
import threading
from pathlib import Path

import serial

SERIAL_PORT = os.environ.get("DABONES_SERIAL_PORT", "/dev/serial0")
BAUD_RATE = int(os.environ.get("DABONES_BAUD_RATE", "115200"))
SONG_DIR = Path(
    os.environ.get("DABONES_SONG_DIR", "/home/pi/dabones/songs")
).resolve()

APLAY = os.environ.get("DABONES_APLAY", "/usr/bin/aplay")
SERIAL_TIMEOUT = 0.2
MAX_LINE_LENGTH = 512
STOP_TIMEOUT = 2.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("dabones-audio")


class AudioService:
    def __init__(self):
        self.selected_file = None
        self.player = None
        self.stopping = threading.Event()

    def state(self):
        """Update the playback state and return a description."""
        if self.player is not None:
            rc = self.player.poll()
            if rc is not None:
                log.info("aplay exited with status %s", rc)
                self.player = None

        return "playing" if self.player is not None else "idle"

    def handle(self, line):
        """Process one complete command and return one response."""
        parts = line.strip().split(maxsplit=1)
        if not parts:
            return "ERR EMPTY_COMMAND"

        command = parts[0].upper()
        argument = parts[1].strip() if len(parts) == 2 else None

        if command == "PING":
            return "OK PONG"

        if command == "LOAD":
            if not argument:
                return "ERR MISSING_FILENAME"

            if self.state() == "playing":
                return "ERR PLAYBACK_ACTIVE"

            # Accept a filename, never a directory or arbitrary path.
            if (
                argument in (".", "..")
                or "/" in argument
                or "\\" in argument
                or "\x00" in argument
            ):
                return "ERR INVALID_FILENAME"

            candidate = SONG_DIR / argument

            try:
                resolved = candidate.resolve(strict=True)
            except (OSError, RuntimeError):
                return "ERR FILE_NOT_FOUND"

            if resolved.parent != SONG_DIR or not resolved.is_file():
                return "ERR INVALID_FILE"

            if not os.access(resolved, os.R_OK):
                return "ERR FILE_NOT_READABLE"

            self.selected_file = resolved
            log.info("Selected audio file: %s", resolved.name)
            return f"OK LOADED {resolved.name}"

        if command == "START":
            if argument:
                return "ERR UNEXPECTED_ARGUMENT"

            if self.state() == "playing":
                return "ERR ALREADY_PLAYING"

            if self.selected_file is None:
                return "ERR NO_FILE_SELECTED"

            try:
                self.player = subprocess.Popen(
                    [APLAY, "-q", str(self.selected_file)],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    close_fds=True,
                )
            except OSError as exc:
                self.player = None
                log.exception("Could not start aplay")
                return f"ERR APLAY_START_FAILED {exc.errno}"

            log.info(
                "Started %s (pid %s)",
                self.selected_file.name,
                self.player.pid,
            )
            return f"OK STARTED {self.selected_file.name}"

        if command == "STOP":
            if argument:
                return "ERR UNEXPECTED_ARGUMENT"

            self.stop_player()
            return "OK STOPPED"

        if command == "STATUS":
            if argument:
                return "ERR UNEXPECTED_ARGUMENT"

            state = self.state()
            filename = (
                self.selected_file.name
                if self.selected_file is not None
                else "none"
            )
            pid = self.player.pid if self.player is not None else 0
            return f"OK STATUS state={state} file={filename} pid={pid}"

        return "ERR UNKNOWN_COMMAND"

    def stop_player(self):
        """Stop aplay gracefully, then force it to exit if necessary."""
        player = self.player
        if player is None:
            return

        self.player = None

        if player.poll() is not None:
            return

        player.terminate()
        try:
            player.wait(timeout=STOP_TIMEOUT)
        except subprocess.TimeoutExpired:
            player.kill()
            player.wait()

        log.info("Stopped aplay")

    def run(self):
        """Run until systemd stops the service."""
        SONG_DIR.mkdir(parents=True, exist_ok=True)

        log.info(
            "Opening UART %s at %d baud; songs: %s",
            SERIAL_PORT,
            BAUD_RATE,
            SONG_DIR,
        )

        with serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=SERIAL_TIMEOUT,
            write_timeout=1.0,
        ) as uart:
            # Discard stale bytes left over from boot or a Pico reset.
            uart.reset_input_buffer()
            uart.write(b"OK READY\n")

            line = bytearray()
            discarding = False

            while not self.stopping.is_set():
                byte = uart.read(1)
                if not byte:
                    self.state()
                    continue

                if byte == b"\n":
                    if discarding:
                        uart.write(b"ERR LINE_TOO_LONG\n")
                    else:
                        command_line = line.decode(
                            "utf-8", errors="replace"
                        ).rstrip("\r")
                        response = self.handle(command_line)
                        log.info("Command: %s -> %s", command_line, response)
                        uart.write((response + "\n").encode("utf-8"))

                    line.clear()
                    discarding = False
                    continue

                if discarding:
                    continue

                if len(line) >= MAX_LINE_LENGTH:
                    line.clear()
                    discarding = True
                    continue

                line.extend(byte)

    def shutdown(self, signum=None, frame=None):
        log.info("Shutdown requested")
        self.stopping.set()
        self.stop_player()


def main():
    service = AudioService()
    signal.signal(signal.SIGTERM, service.shutdown)
    signal.signal(signal.SIGINT, service.shutdown)

    try:
        service.run()
    finally:
        service.stop_player()
        log.info("Audio service exited")


if __name__ == "__main__":
    main()
