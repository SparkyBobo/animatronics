"""
DaBones

Tickles deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.tickles import Tickles
from dabones.show.context import ShowContext

context = ShowContext()
performer = Tickles(context)
context.run()