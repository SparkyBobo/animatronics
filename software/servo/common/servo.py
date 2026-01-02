#
# Animatroincs Servo Module
# Copyright (C) 2025 Sparky Bobo Designs
# https://github.com/SparkyBobo/animatronics/tree/master/software/midi
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
# About Animatroincs Midi Module
#
# The Animatroincs Servo Module (ANI-SRV) is a CircuitPython program designed
# for use with the the Animatroincs Midi Module (ANI-MID) and the Animatroincs
# DMX Module (ANI-DMX). The ANI-SRV program receives MIDI notes from a controller
# or sequencer and controls the servos and LEDs of a character.
#
import board
import digitalio
import pwmio

# create a PWMOut object on Pin GP0.
pwmCount = 16
pwmPins = [ board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15 ]
pwmFrequency = 50
pwmDutyCycle = 2 ** 15
pwms = []
servos = []
for n in range(0, pwmCount):
    pwm = pwmio.PWMOut(pwmPins[n], duty_cycle=pwmDutyCycle, frequency=pwmFrequency)
    pwms.insert(n, pwm)
    servos.insert(n, servo.Servo(pwm))
    print("Servo ", n, " on pin: ", pwmPins[n])

# Get angle
def getAngle(servo):
    if (servo >= 0 and servo < pwmCount):
        return servos[servo].angle
    return -1

# Set angle
def setAngle(servo,angle):
    if (servo >= 0 and servo < pwmCount):
        if (angle >= 0 and angle <= 180):
            servos[servo].angle = angle

