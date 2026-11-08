"""
Animacy

Driver color contract.

Copyright (c) 2026 Sparky Bobo
"""

class Color:
    """
    Represents a color in RGBW.

    Attributes:
        red: The red amount
        green: The green amount
        blue: The blue amount
        white: The white amount
    """
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0, white: int = -1):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.white = white

    def __str__(self) -> str:
        if (self.white >= 0):
            return f"Color({self.red}:{self.green}:{self.blue}:{self.white})"
        return f"Color({self.red}:{self.green}:{self.blue})"

