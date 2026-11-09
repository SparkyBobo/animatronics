"""
Animacy

Tickles deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.tickles import Tickles
from animacy.show.context import ShowContext

context = ShowContext()
performer = Tickles(context)
context.run()
