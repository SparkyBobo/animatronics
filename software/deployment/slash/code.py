"""
DaBones

Slash deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.slash
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.slash.Slash(context)
context.run()
