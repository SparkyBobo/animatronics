"""
Animacy

CircuitPython pin map utility.

Copyright (c) 2026 Sparky Bobo
"""

import board
import microcontroller

board_pins = []
for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append(f"board.{alias}")
        # Add the original GPIO name, in parentheses.
        if pins:
            # Only include pins that are in board.
            pins.append(f"({pin!s})")
            board_pins.append(" ".join(pins))

for pins in sorted(board_pins):
    print(pins)
