"""
DaBones

Beats deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.beats import Beats
from dabones.show.context import ShowContext

context = ShowContext()
performer = Beats(context)
context.run()