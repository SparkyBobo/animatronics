"""
Animacy

Desktop shim for rp2pio.

Copyright (c) 2026 Sparky Bobo
"""

class StateMachine:
    """StateMachine shim."""

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.active = True

    def deinit(self):
        self.active = False

    def background_write(self, *, loop=None) -> None:
        self.last_write = loop
