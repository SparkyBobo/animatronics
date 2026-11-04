"""
DaBones

LizzieB deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.lizzie
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.lizzie.LizzieB(context)
context.run()
