"""
Animacy

Audio deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.audio import Audio
from animacy.show.context import ShowContext

context = ShowContext()
performer = Audio(context)
context.run()
