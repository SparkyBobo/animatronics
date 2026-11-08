"""
Animacy

LizzieB deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.lizzie import LizzieB
from animacy.show.context import ShowContext

context = ShowContext()
performer = LizzieB(context)
context.run()