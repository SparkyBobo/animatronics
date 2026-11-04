"""
DaBones

LizzieB deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.lizzie import LizzieB
from dabones.show.context import ShowContext

context = ShowContext()
performer = LizzieB(context)
context.run()