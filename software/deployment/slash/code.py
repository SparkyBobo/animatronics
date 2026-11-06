"""
DaBones

Slash deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.slash import Slash
from animacy.show.context import ShowContext

context = ShowContext()
performer = Slash(context)
context.run()