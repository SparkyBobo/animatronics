"""
DaBones

Audio deployment.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.characters.audio import Audio
from dabones.show.context import ShowContext

context = ShowContext()
performer = Audio(context)
context.run()
