"""
DaBones

Groove deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.groove
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.groove.Groove(context)
context.run()
