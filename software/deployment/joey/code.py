"""
Animacy

Joey deployment.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.joey import Joey
from animacy.show.context import ShowContext

context = ShowContext()
performer = Joey(context)
context.run()