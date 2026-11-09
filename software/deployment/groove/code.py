"""
Animacy

Groove deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.groove import Groove
from animacy.show.context import ShowContext

context = ShowContext()
performer = Groove(context)
context.run()
