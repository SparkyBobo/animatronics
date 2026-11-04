"""
DaBones

Slash deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.slash import Slash
from dabones.show.context import ShowContext

context = ShowContext()
performer = Slash(context)
context.run()