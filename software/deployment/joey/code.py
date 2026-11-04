"""
DaBones

Joey deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.joey import Joey
from dabones.show.context import ShowContext

context = ShowContext()
performer = Joey(context)
context.run()