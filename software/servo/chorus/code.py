#
# Animatroincs Chorus Singers Module
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
# About Animatroincs Chorus Singers Module
#
# The Animatroincs Servo Module (ANI-SRV) is a CircuitPython board designed
# to control servos. This module is the definition of the chorus singers'
# leds and motors.
import servo
import motion

mouth1 = Motion() # Micro Servo
mouth2 = Motion() # Micro Servo
mouth3 = Motion() # Micro Servo
mouths = [ mouth1, mouth2, mouth3 ]

headPan1 = Motion() # Speed Servo
headPan2 = Motion() # Speed Servo
headPan3 = Motion() # Speed Servo
headPan = [ headPan1, headPan2, headPan3 ]

leftEye1 = RgbLed()
rightEye1 = RgbLed()
leftEye2 = RgbLed()
rightEye2 = RgbLed()
leftEye3 = RgbLed()
rightEye3 = RgbLed()
leftEyes = [ leftEye1, leftEye2, leftEye3 ]
rightEyes = [ rightEye1, rightEye2, rightEye3 ]
bothEyes = [ [ leftEye1, rightEye1], [ leftEye2, rightEye2, ] [ leftEye3, rightEye3 ] ]

upLight1 = PowerLed()
upLight2 = PowerLed()
upLight3 = PowerLed()
upLights = [ upLight1, upLight2, upLight3 ]
