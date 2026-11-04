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

# Common Imports
import board
import busio
import digitalio
import analogio
import pwmio
import time
import array
from math import floor

# Midi Imports
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.midi_continue import Continue
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop

# Motor
from adafruit_motor import servo

# NeoPixel Imports.
import neopixel
from rainbowio import colorwheel

# Setup status LED
picoLed = digitalio.DigitalInOut(board.LED)
picoLed.direction = digitalio.Direction.OUTPUT
picoLed.value = True

# Setup MIDI device on UART
uart = busio.UART(board.GP16, board.GP17, baudrate=31250, timeout=0.001)
midi_uart = adafruit_midi.MIDI(midi_in=uart)
print("Setup MIDI device on UART.")

# Create PWMOut objects
pwmCount = 12
pwmPins = [ board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11 ]
pwmFrequency = 50
pwmDutyCycle = 2 ** 15
pwms = []
servos = []
servo_default = [0, 105, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]  # Default servo positions for servos 0-11
for n in range(0, pwmCount):
    pwm = pwmio.PWMOut(pwmPins[n], duty_cycle=pwmDutyCycle, frequency=pwmFrequency)
    pwms.insert(n, pwm)
    if (n < 12):   # Only create servos for first 12 channels
        servos.insert(n, servo.Servo(pwm, min_pulse=750, max_pulse=2250))
        servos[n].angle = servo_default[n]
        print("Servo ", n, " on pin: ", pwmPins[n])

motorCount = 2
motorPins = [ board.GP13, board.GP14 ]
motorFrequency = 2000  
motors = []
for n in range(0, motorCount):  
    motor = pwmio.PWMOut(motorPins[n], frequency=motorFrequency)    
    motors.insert(n, motor)
    motor.duty_cycle = 0
    print("Motor ", n, " on pin: ", motorPins[n])

SLP = digitalio.DigitalInOut(board.GP15)
SLP.switch_to_output()    

# Enable DRV8833
SLP.value = True

# Neopixels
pixel_count = 3
pixels = neopixel.NeoPixel(board.GP22, pixel_count)

# Display
i2c0 = busio.I2C(board.GP21, board.GP20)
#displayio.release_displays()
#display_bus = I2CDisplayBus(i2c0, device_address=0x3D)

# Spare I2C for other devices
i2c1 = busio.I2C(board.GP19, board.GP18)

# Eyes
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

# Loop
while True:

    #  receive MIDI input
    msg=midi_uart.receive()

    #  if the input is a recognized message...
    if msg is not None:
        if isinstance(msg, NoteOn):
             picoLed.value = True

        if isinstance(msg, NoteOff):
            picoLed.value = False

        if isinstance(msg, ControlChange):
            picoLed.value = not picoLed.value
            print("CC: ", msg.control, "Value:", msg.value)
            if (msg.control >= 70) and (msg.control < 72):
                servo_index = msg.control - 70
                servos[servo_index].angle = floor(msg.value * 180 // 127)
                print("Servo ", servo_index, " angle: ", servos[servo_index].angle)
            elif (msg.control >= 72) and (msg.control < 74):
                motor_index = msg.control - 72
                motors[motor_index].duty_cycle = (msg.value << 8) + 25600
                print("Motor ", motor_index, " duty_cycle: ", motors[motor_index].duty_cycle)
            elif (msg.control >= 74) and (msg.control < 75):
                pixels.brightness = msg.value / 127.0
                print("Brightness: ", pixels.brightness)

        if isinstance(msg, ProgramChange):
            picoLed.value = not picoLed.value

        if isinstance(msg, NoteOn) and msg.velocity != 0:
            print("noteOn: ", msg.note, "vel:", msg.velocity)

            if (msg.note == 36):
                pixels.fill(RED)
                pixels.show()
            elif (msg.note == 37):
                pixels.fill(GREEN)
                pixels.show()
            elif (msg.note == 38):
                pixels.fill(BLUE)
                pixels.show()
            elif (msg.note == 39):
                pixels.fill(YELLOW)
                pixels.show()
            elif (msg.note == 40):
                pixels.fill(CYAN)
                pixels.show()
            elif (msg.note == 41):
                pixels.fill(PURPLE)
                pixels.show()
            elif (msg.note == 42):
                servos[0].angle = msg.velocity
            elif (msg.note == 43):
                servos[1].angle = msg.velocity

        elif (isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0)):
            print("noteOff:", msg.note, "vel:", msg.velocity)            
            if (msg.note == 42):
                servos[0].angle = servo_default[0]
            if (msg.note == 43):
                servos[1].angle = servo_default[1]

