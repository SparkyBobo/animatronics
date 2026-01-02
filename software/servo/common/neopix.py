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
import busio
import digitalio
import pwmio
from microcontroller import Pin
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

from adafruit_motor import servo

import neopixel


# Setup status LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# Setup MIDI device on UART
uart = busio.UART(board.GP16, board.GP17, baudrate=31250, timeout=0.001)
midi_controller = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, out_channel=0)
print("Setup USB MIDI device on UART.")

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

# Setup neopixel
pixel_pin = board.GP22
num_pixels = 12
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)
print("NeoPixel on pin: ", pixel_pin, ", count: ", num_pixels)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
color = GREEN
color_red = 0
color_green = 255
color_blue = 0

# Loop
while True:

    #  array of message types
    messages = (NoteOn, NoteOff, PitchBend, ControlChange)

    #  receive MIDI input from UART
    msg=midi_controller.receive()

    #  if the input is a recognized message...
    if msg is not None:
        if isinstance(msg, NoteOn):
            led.value = True
            pixels.fill(RED)
            pixels.show()    
            if ((msg.note % 2) == 0):
                for n in range(0, pwmCount):
                    servos[n].angle = 0
            if ((msg.note % 2) == 1):
                for n in range(0, pwmCount):
                    servos[n].angle = 180


        if isinstance(msg, NoteOff):
            led.value = False
            pixels.fill(color)
            pixels.show()    
            for n in range(0, pwmCount):
                servos[n].angle = 90

        if isinstance(msg, ControlChange):
            if ((msg.control % 4) == 1):
                color_red = msg.value * 2

            if ((msg.control % 4) == 2):
                color_green = msg.value * 2

            if ((msg.control % 4) == 3):
                color_blue = msg.value * 2

            color = (color_red, color_green, color_blue)
            pixels.fill(color)
            pixels.show()    

