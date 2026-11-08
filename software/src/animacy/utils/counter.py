"DriverValue""""
Animacy

Incrementing counter.

Copyright (c) 2026 Sparky Bobo
"""

class Counter:
    def __init__(self, start=0):
        self.value = start

    def __next__(self):
        value = self.value
        self.value += 1
        return value