"""
DaBones

Groove deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.groove import Groove
from dabones.show.context import ShowContext

context = ShowContext()
performer = Groove(context)
context.run()