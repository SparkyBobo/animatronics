#
# Animatroincs Guitar Player Module
# Copyright (C) 2025 Sparky Bobo Designs
# https://github.com/SparkyBobo/animatronics/tree/master/software/servo/guitar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# About Animatroincs Guitar Player Module
#
# The Animatroincs Servo Module (ANI-SRV) is a CircuitPython board designed
# to control servos. This module is the definition of the guitar players
# leds and motors.
import servo
import motion

strum = Motion() # Speed servo
slide = Motion() # Speed servo
rotate = Motion() # Torque servo
fretFinger1 = Motion() # Micro servo
fretFinger2 = Motion() # Micro servo
fretFinger3 = Motion() # Micro servo
fretFingers = [ fretFinger1, fretFinger2, fretFinger3 ]
footTap = Motion() # Micro servo

leftEye = RgbLed()
leftRight = RgbLed()

upLight = PowerLed()
