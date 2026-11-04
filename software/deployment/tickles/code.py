"""
DaBones

Tickles deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.tickles
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.tickles.Tickles(context)
context.run()
