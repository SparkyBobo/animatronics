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
import time
import board
import busio
import digitalio

# USB/Midi Imports
import usb.core
import usb_midi
import adafruit_midi
import adafruit_usb_host_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

# Display Imports
import displayio
import terminalio
from i2cdisplaybus import I2CDisplayBus
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297
from adafruit_display_text import bitmap_label as label

# Setup status LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

led_usb_host = digitalio.DigitalInOut(board.GP1)
led_usb_host.direction = digitalio.Direction.OUTPUT
led_usb_host.value = False

led_usb = digitalio.DigitalInOut(board.GP0)
led_usb.direction = digitalio.Direction.OUTPUT
led_usb.value = False

# Display
i2c0 = busio.I2C(board.GP21, board.GP20)

# Spare I2C for other devices
i2c1 = busio.I2C(board.GP19, board.GP18)

# Setup MIDI device on UART, all channels
# In from external controller via DIN, out to TRS.
uart = busio.UART(board.GP16, board.GP17, baudrate=31250, timeout=0.001)
midi_uart = adafruit_midi.MIDI(midi_in=uart, midi_out=uart)
print("Setup MIDI device on UART.")

# Setup MIDI device on USB, all channels.
midi_usb = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])
print("Setup MIDI device on USB.")

# Setup USB Host for MIDI, all channels.
usb_host = None
usb_check_period = 5.0  # seconds
last_usb_check_time = time.monotonic() - usb_check_period
midi_usb_host = None

# Prcoess midi messages
def process_midi_message(msg):
    if msg is not None:
        if isinstance(msg, NoteOn):
            midi_uart.send(msg)
            print("Note On:", msg.note, "Velocity:", msg.velocity)

        if isinstance(msg, NoteOff):
            midi_uart.send(msg)
            print("Note Off:", msg.note, "Velocity:", msg.velocity)

        if isinstance(msg, PitchBend):
            midi_uart.send(msg)
            print("Pitch Bend:", msg.control, "Value:", msg.value)

        if isinstance(msg, ControlChange):
            midi_uart.send(msg)
            print("Control Change:", msg.program)

# Loop
while True:

    # Check for USB MIDI device every usb_check_period seconds
    usb_check_time = time.monotonic()
    if usb_check_time - last_usb_check_time >= usb_check_period:
        last_usb_check_time = usb_check_time
        print("Checking for USB MIDI device...")
        if (usb_host == None):
            for device in usb.core.find(find_all=True):
                try:
                    usb_host = adafruit_usb_host_midi.MIDI(device)
                    midi_usb_host = adafruit_midi.MIDI(midi_in=usb_host)
                    led_usb_host.value = True
                    print("Found USB MIDI device:", device.manufacturer, device.product, "VID:", hex(device.idVendor), "PID:", hex(device.idProduct))
                    break
                except ValueError:
                    continue
        else:
            existing_usb_host = usb.core.find(idVendor=usb_host.device.idVendor, idProduct=usb_host.device.idProduct)
            if (existing_usb_host is None):
                print("USB MIDI device disconnected.")
                usb_host = None
                midi_usb_host = None
                led_usb_host.value = False

    #  array of message types
    messages = (NoteOn, NoteOff, PitchBend, ControlChange)

    #  receive MIDI input
    msg_uart = midi_uart.receive()
    if msg_uart is not None:
        process_midi_message(msg_uart)
        led.value = not led.value

    msg_usb = midi_usb.receive()
    if msg_usb is not None:
        process_midi_message(msg_usb)
        led_usb.value = not led_usb.value

    if (midi_usb_host is not None):
        msg_usb_host = midi_usb_host.receive()
        if msg_usb_host is not None:
            process_midi_message(msg_usb_host)
            led_usb_host.value = not led_usb_host.value


