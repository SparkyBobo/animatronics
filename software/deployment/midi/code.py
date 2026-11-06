#
# Animatroincs Midi Module
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
# The Animatroincs Midi Module (ANI-MID) is a CircuitPython program designed
# for use with the the Animatroincs Midi Module (ANI-MID). The ANI-MID program
# receives MIDI notes from a controller or sequencer and sends the note data
# to the ANI-SRV and ANI-DMX modules.
#

# Common Imports
import board
import busio
import digitalio
import time

# DaBones Imports
from animacy.midi.messages import *

# USB/Midi Imports
import usb_host
import usb.core
import usb_midi
import adafruit_midi
import adafruit_usb_host_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.midi_continue import Continue
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock

# Setup status LEDs
picoLed = digitalio.DigitalInOut(board.LED)
picoLed.direction = digitalio.Direction.OUTPUT
picoLed.value = True

led_usb_host = digitalio.DigitalInOut(board.GP1)
led_usb_host.direction = digitalio.Direction.OUTPUT
led_usb_host.value = True

led_usb_dev = digitalio.DigitalInOut(board.GP0)
led_usb_dev.direction = digitalio.Direction.OUTPUT
led_usb_dev.value = True

# Setup USB Host for MIDI, all channels.
usb_host_device = None
midi_usb_host = None

# Setup the Type-A USB Port for the USB Midi Host
# Give the host stack time to enumerate on cold boot
usb_host.Port(board.GP4, board.GP5)
time.sleep(2.0)

# Find any MIDI devices on the Type-A USB port
# The USB Host MIDI library does not support hot-plugging, 
# so if the device is lost it will need to be reconnected 
# to be found again.
if usb_host_device is None:
    print("Looking for devices on USB Host...")
    for device in usb.core.find(find_all=True):
        try:
            print("Found: manufacturer", device.manufacturer, "product", device.product, "serial", device.serial_number, "vid", hex(device.idVendor), "product", hex(device.idProduct))
            usb_host_device=adafruit_usb_host_midi.MIDI(device, timeout=0.001)
        except ValueError:
            continue

        if (usb_host_device is None):
            print("Not Found: no midi devices found")
        else:
            print("Setup MIDI device on usb host.")
            midi_usb_host = adafruit_midi.MIDI(midi_in=usb_host_device, debug=True)
            led_usb_host.value = False        

# Setup MIDI device on UART, all channels
# In from external controller via DIN, out to TRS.
uart = busio.UART(board.GP16, board.GP17, baudrate=31250, timeout=0.001)
midi_uart = adafruit_midi.MIDI(midi_in=uart, midi_out=uart)
print("Setup MIDI device on UART.")

# Setup MIDI device on USB, all channels.
midi_usb_dev = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])
print("Setup MIDI device on USB.")

# Display
i2c0 = busio.I2C(board.GP21, board.GP20)

# Spare I2C for other devices
i2c1 = busio.I2C(board.GP19, board.GP18)

# MIDI Recieve function
def midi_receive(midi_dev, midi_led=None):

    # Exit if the device is not set.
    if midi_dev is None:
        return    

    #  Receive MIDI input and retransmit
    msg=midi_dev.receive()
    if msg is not None:
        if (midi_led is not None):
            midi_led.value = not midi_led.value
        midi_debug(msg)
        return msg
    return None

# MIDI Forwarding function
def midi_forward(midi_dev, midi_led=None):
    msg = midi_receive(midi_dev, midi_led)
    if msg is not None:
        midi_uart.send(msg)
        midi_debug(msg)

# MIDI Forwarding function
def midi_debug(msg):
    if msg is not None:
        if isinstance(msg, NoteOn):
            print("MIDI NoteOn ",msg.channel,":",msg.note,":",msg.velocity)

        elif isinstance(msg, NoteOff):
            print("MIDI NoteOff ",msg.channel,":",msg.note,":",msg.velocity)

        elif isinstance(msg, ControlChange):
            print("MIDI ControlChange ",msg.channel,":",msg.control,":",msg.value)

        elif isinstance(msg, ProgramChange):
            print("MIDI ProgramChange ",msg.channel,":",msg.patch)

        elif isinstance(msg, PitchBend):
            print("MIDI PitchBend ",msg.channel,":",msg.pitch_bend)

        elif isinstance(msg, Start):
            print("MIDI Start ",msg.channel)

        elif isinstance(msg, Stop):
            print("MIDI Stop ",msg.channel)

        elif isinstance(msg, Continue):
            print("MIDI Continue ",msg.channel)

# Midi Setup
CLOCK_INTERVAL = 60.0 / (120 * 24)  # 20.833 ms
next_clock_tick = -1
midi_clock_enable = False

# Midi start delays
start_delays = [0,-225,0,0,0]
start_delay = start_delays[1]

# Loop
while True:

    #  receive MIDI input from USB Device
    midi_forward(midi_usb_dev, led_usb_dev)

    #  receive MIDI input from UART
    midi_forward(midi_uart)

    # receive MIDI input from USB Host
    control_msg = None
    try:
        control_msg = midi_receive(midi_usb_host, led_usb_host)
    except usb.core.USBError:
        print("Lost USB Host MIDI device.")
        usb_host_device = None
        midi_usb_host = None
        led_usb_host.value = True

    # Process show control messages.
    if control_msg is not None:
        
        if isinstance(control_msg, NoteOn):
            if (control_msg.note == 8):
                midi_uart.send(NoteOn(channel=0, note=1, velocity=127))
                midi_uart.send(NoteOff(channel=0, note=1, velocity=127))
            if (control_msg.note == 7):
                midi_uart.send(NoteOn(channel=0, note=2, velocity=127))
                midi_uart.send(NoteOff(channel=0, note=2, velocity=127))
            if (control_msg.note >= 5 and control_msg.note <= 6):
                song = control_msg.note-4
                print("Select song ", song)
                midi_clock_enable = False
                midi_uart.send(SongSelect(song))
                start_delay = start_delays[song]
            elif (control_msg.note == 4):
                print("Start Clock")
                midi_uart.send(Start(channel=0))
                midi_clock_enable = True
                next_clock_tick = time.monotonic() + CLOCK_INTERVAL
            elif (control_msg.note == 3):
                print("Start Song ")
                midi_clock_enable = False
                midi_uart.send(Start(channel=0))
            elif (control_msg.note == 2):
                print("Stop Song ")
                midi_clock_enable = False
                midi_uart.send(Stop(channel=0))
            elif (control_msg.note == 1):
                print("System Reset")
                midi_clock_enable = False
                song_stop = Stop(channel=0)
                midi_uart.send(song_stop)
                midi_debug(song_stop)

        elif isinstance(control_msg, ControlChange):
                print("Control Change")
                midi_uart.send(ControlChange(control=control_msg.control, value=control_msg.value, channel=0))

    # Send the midi clock if enabled.
    if midi_clock_enable:
         next_tick = time.monotonic()
         if (next_tick >= next_clock_tick):
             if (start_delay < 0):
                 start_delay += 1
             else:
                 # Send the starting clock pulse
                 midi_uart.send(TimingClock())
                 midi_clock_enable = False
                 print("Send sync pulse")
             next_clock_tick += CLOCK_INTERVAL

