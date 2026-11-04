"""
DaBones

Audio deployment.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.characters.audio
import dabones.show.context

context = dabones.show.context.ShowContext()
performer = dabones.characters.audio.Audio(context)
context.run()
