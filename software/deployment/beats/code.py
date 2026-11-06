"""
DaBones

Beats deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.beats import Beats
from animacy.show.context import ShowContext

context = ShowContext()
performer = Beats(context)
context.run()