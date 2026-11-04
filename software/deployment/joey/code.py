"""
DaBones

Joey deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.joey
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.joey.Joey(context)
context.run()
