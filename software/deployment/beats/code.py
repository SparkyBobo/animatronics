"""
DaBones

Beats deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.beats
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.beats.Beats(context)
context.run()
