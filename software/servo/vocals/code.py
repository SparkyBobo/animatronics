#
# Animatroincs Singer Module
# Copyright (C) 2025 Sparky Bobo Designs
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
# to control servos. This module is the definition of the singers
# leds and motors.
import servo
import motion

mouth = Motion() # Speed servo
headPan = Motion() # Speed servo
handTap = Motion() # Micro servo
footTap = Motion() # Micro servo
micStand = Motion() # Torque servo
hips = Motion() # Speed servo
leftArm = Motion() # Speed servo
rightArm = Motion() # Speed servo

leftEye = RgbLed()
leftRight = RgbLed()

upLight = PowerLed()
