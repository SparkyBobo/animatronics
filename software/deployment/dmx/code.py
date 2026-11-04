#
# Animatroincs Dmx Module
# Copyright (C) 2025 Sparky Bobo Designs
# https://github.com/SparkyBobo/animatronics/tree/master/software/dmx
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
# About Animatroincs Dmx Module
#
# The Animatroincs Dmx Module (ANI-DMX) is a CircuitPython program designed
# for use with the the Animatroincs Dmx Module (ANI-DMX). The ANI-DMX program
# receives MIDI notes from a controller or sequencer and sends the note data
# to DX-512, NeoPixels, and Motors.
#

# Common Imports
import board
import busio
import digitalio
import array
import time
import rp2pio
import adafruit_pioasm

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

# Setup MIDI device on UART
uart = busio.UART(board.GP16, board.GP17, baudrate=31250, timeout=0.001)
midi_uart = adafruit_midi.MIDI(midi_in=uart)
my_midi_channel = 13
print("Setup MIDI device on UART, primary channel ", my_midi_channel, ".")

# Setup dmx
DMX_CHANNELS = 320
mode_pin_num = board.GP7
out_pin = board.GP8
timing_pin = board.GP4

white_start_value = 0
white_target_value = 0
white_current_value = 0
white_start_time = time.monotonic()
white_duration = 1

red_start_value = 0
red_target_value = 0
red_current_value = 0
green_start_value = 0
green_target_value = 0
green_current_value = 0
blue_start_value = 0
blue_target_value = 0
blue_current_value = 0
rgb_start_time = time.monotonic()
rgb_duration = 1

red = 0
green = 0
blue = 0
white = 0
next_clock_tick = time.monotonic()
clock_internal = 60.0 / (120 * 24)  # 20.833 ms, midi clock rate
fade_seconds = .001

# Initialize mode pin
dmx_mode_pin = digitalio.DigitalInOut(mode_pin_num)
dmx_mode_pin.direction = digitalio.Direction.OUTPUT
dmx_mode_pin.value = True  # Set to transmit

# Initialize DMX values buffer
# Array structure: [MBB, BRK, MAB, channel_count, start_code, ch1_data, ch2_data, ...]
dmx_values = array.array("L", (0 for _ in range(DMX_CHANNELS + 5)))

# Setup tx timings - See https://support.etcconnect.com/ETC/FAQ/DMX_Speed
# These timings are close to the Eos family of products "medium" speed.
dmx_values[0] = 30            # Word 0: Length of MARK BEFORE BREAK in microseconds (8us min)
dmx_values[1] = 142           # Word 1: Length of SPACE FOR BREAK in microseconds (92us min)
dmx_values[2] = 128           # Word 2: Length of MARK AFTER BREAK in microseconds (12us min)
dmx_values[3] = DMX_CHANNELS  # Word 3: Number of channels to send (1-512) + (1 for start code)
dmx_values[4] = 0             # Word 4: Start Code data byte (usually 0)
DMX_VALUES_INDEX0 = 5

# DMX PIO program - Borrowed heavily from [mydana]: https://github.com/mydana/CircuitPython_DMX_Transmitter
dmx_tx_program = adafruit_pioasm.Program(
    """
    ;Labels:          OPCODES                   Side Bits   Delay  Interval  Comments
    .program dmx512tx
    .side_set 3
    .wrap_target
        next_frame:
                    mov pins, ~ null            side 0b110         ;MAB      ; MARK AFTER BREAK
                    out x, 16                   side 0b110         ;MBB      ; MARK BEFORE BREAK: microseconds
    mark_before_break:
                    jmp x--, mark_before_break  side 0b110         ;MBB      ; MARK BEFORE BREAK: (MBB)

                    mov pins, null              side 0b101         ;BRK      ; SPACE FOR BREAK
                    out x, 16                   side 0b101         ;BRK      ; SPACE FOR BREAK: microseconds
    space_for_break:
                    jmp x--, space_for_break    side 0b101         ;BRK      ; SPACE FOR BREAK (BRK)

                    mov pins, ~ null            side 0b011         ;MAB      ; MARK AFTER BREAK
                    out x, 16                   side 0b011         ;BRK      ; MARK AFTER BREAK: microseconds
    mark_after_break:
                    jmp x--, mark_after_break   side 0b011         ;MAB      ; MARK AFTER BREAK: (MAB)

    load_channel_count:
                    out y, 16                   side 0b111         ;MAB      ; Ctrl: Get the number of slots we'll display
    data_byte:
                    mov pins, null              side 0b111  [2]    ;STA      ; DATA: Start bit (STA)
                    set x, 7                    side 0b111         ;STA      ; DATA: Set up 8 bits
    data_bit:
                    out pins, 1                 side 0b111  [2]    ;DAT      ; DATA: Data bit (DAT)
                    jmp x--, data_bit           side 0b111         ;DAT      ; DATA: more bits

                    mov pins, ~ null            side 0b111         ;STP      ; MARK_BETWEEN_SLOTS
                    out null, 8                 side 0b111         ;DAT      ; DATA: Toss out the rest of the word & trigger auto-pull.
                    set x, 13                   side 0b111         ;STP      ; MARK_BETWEEN_SLOTS: 16 microseconds (3 cycle setup + 13 loop)
    data_stop:
                    jmp x--, data_stop          side 0b111         ;STP      ; MARK_BETWEEN_SLOTS: (STP)

    channel_next:
                    jmp y--, data_byte          side 0b111         ;STP      ; Ctrl: Count down the slots.
    .wrap
    """
)

# Setup the tx state machine environment
dmx_state_machine = rp2pio.StateMachine(
    program=dmx_tx_program.assembled,
    frequency=1_000_000,
    first_out_pin=out_pin,
    out_pin_count=1,
    initial_out_pin_state=1,
    first_sideset_pin=timing_pin,
    sideset_pin_count=3,
    initial_sideset_pin_state=7,
    exclusive_pin_use=True,
    pull_threshold=16,
    auto_pull=True,
    out_shift_right=True
)

# Start background transmission
dmx_state_machine.background_write(loop=memoryview(dmx_values))

def all_off():
    """Turn off all DMX channels"""
    for i in range(DMX_CHANNELS):
        dmx_values[DMX_VALUES_INDEX0 + i] = 0

def white_fade(target):
    white_start_value = dmx_values[DMX_VALUES_INDEX0]
    white_target_value = target * 2
    white_start_time = time.monotonic()
    white_duration = fade_seconds

# Loop
while True:

    #  receive MIDI input
    msg=midi_uart.receive()

    #  if the input is a recognized message...
    if msg is not None:
        if msg.channel == 0 or msg.channel == my_midi_channel:

            if isinstance(msg, Start) or (isinstance(msg, NoteOn) and msg.note == 1):
                print("Start")
                white_fade(white)

                red_start_value = dmx_values[DMX_VALUES_INDEX0 + 101 + 0]
                red_target_value = red
                green_start_value = dmx_values[DMX_VALUES_INDEX0 + 101 + 1]
                green_target_value = green
                blue_start_value = dmx_values[DMX_VALUES_INDEX0 + 101 + 2]
                blue_target_value = blue
                rgb_start_time = time.monotonic()
                rgb_duration = fade_seconds


            elif isinstance(msg, Stop) or (isinstance(msg, NoteOn) and msg.note == 2):
                print("Stop")

                red_start_value = dmx_values[DMX_VALUES_INDEX0 + 101 + 0]
                red_target_value = 0
                green_start_value = dmx_values[DMX_VALUES_INDEX0 + 101 + 1]
                green_target_value = 0
                blue_start_value = dmx_values[DMX_VALUES_INDEX0 + 101 + 2]
                blue_target_value = 10
                rgb_start_time = time.monotonic()
                rgb_duration = fade_seconds

            elif isinstance(msg, ControlChange):
                print("CC: ", msg.control, "Value:", msg.value)
                if (msg.control == 20):
                    white_level = msg.value * 2
    
                if (msg.control >= 21 and msg.control <= 23):
                    if (msg.control == 21):
                        red = msg.value * 2
                    if (msg.control == 22):
                        green = msg.value * 2
                    if (msg.control == 23):
                        blue = msg.value * 2

                if (msg.control == 24):
                    if (msg.value == 0):
                        fade_seconds = .001
                    elif (msg.value <= 128):
                        fade_seconds = 0.1 + (msg.value - 1) * 9.9 / 126
                        print(f"Fade set to {fade_seconds}")

    # Fade
    next_tick = time.monotonic()
    if (next_tick >= next_clock_tick):
        if (white_current_value != white_target_value):

            white_elapsed = time.monotonic() - white_start_time
            white_progress = min(1.0, white_elapsed / white_duration)
            white_current_value = round(white_start_value + (white_target_value - white_start_value) * white_progress)
            for channel in range(24):
                dmx_values[DMX_VALUES_INDEX0 + channel - 1] = white_current_value

            if white_progress >= 1.0:
                white_current_value = white_target_value

        if (red_current_value != red_target_value or green_current_value != green_target_value or blue_current_value != blue_target_value):

            rgb_elapsed = time.monotonic() - rgb_start_time
            rgb_progress = min(1.0, rgb_elapsed / rgb_duration)
            red_current_value = round(red_start_value + (red_target_value - red_start_value) * rgb_progress)
            green_current_value = round(green_start_value + (green_target_value - green_start_value) * rgb_progress)
            blue_current_value = round(blue_start_value + (blue_target_value - blue_start_value) * rgb_progress)
            for channel in [101, 111, 121, 131, 201, 211, 301, 311]:
                dmx_values[DMX_VALUES_INDEX0 + channel - 1] = 255
                dmx_values[DMX_VALUES_INDEX0 + channel + 0] = red_current_value
                dmx_values[DMX_VALUES_INDEX0 + channel + 1] = green_current_value
                dmx_values[DMX_VALUES_INDEX0 + channel + 2] = blue_current_value

            if rgb_progress >= 1.0:
                red_current_value = red_target_value
                green_current_value = green_target_value 
                blue_current_value = blue_target_value

        next_clock_tick += clock_internal
