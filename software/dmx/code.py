#
# Animatroincs Dmx Module
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
# About Animatroincs Dmx Module
#
# The Animatroincs Dmx Module (ANI-DMX) is a CircuitPython program designed
# for use with the the Animatroincs Dmx Module (ANI-DMX). The ANI-DMX program
# receives MIDI notes from a controller or sequencer and sends the note data
# to DX-512, NeoPixels, and Motors.
#

# Common Imports
from click import group
import board
import busio
import digitalio
import time
import array

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

# DMX Imports
import rp2pio
import adafruit_pioasm

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

# Setup dmx
dmx_mode_pin = digitalio.DigitalInOut(board.GP7)
dmx_mode_pin.direction = digitalio.Direction.OUTPUT
dmx_mode_pin.value = True  # Set to transmit
dmx_out_pin = board.GP8
dmx_timing_pin = board.GP4

# This value buffer holds what to send to DMX
dmx_channels = 512
dmx_values = array.array("L", (0 for _ in range(dmx_channels + 5)))

# Setup tx timings - See https://support.etcconnect.com/ETC/FAQ/DMX_Speed
# I'm using timings close to the Eos family of products "medium" speed.
dmx_values[0] = 30            ## Word 0: Length of MARK BEFORE BREAK in microseconds (8us min)
dmx_values[1] = 142           ## Word 1: Length of SPACE FOR BREAK in microseconds (92us min)
dmx_values[2] = 128           ## Word 2: Length of MARK AFTER BREAK in microseconds (12us min)
dmx_values[3] = dmx_channels  ## Word 3: Number of channels to send (1-512) + (1 for start code)
dmx_values[4] = 0             ## Word 4: Start Code data byte (usually 0)
dmx_values_index0 = 5          ## First channel index in write_values array

# Neopixels
pixel_count = 2
pixels = neopixel.NeoPixel(board.GP22, pixel_count)

# Display
i2c0 = busio.I2C(board.GP21, board.GP20)
#displayio.release_displays()
#display_bus = I2CDisplayBus(i2c0, device_address=0x3D)

# Spare I2C for other devices
i2c1 = busio.I2C(board.GP19, board.GP18)

# DMX PIO program
# Borrowed heavily from [mydana]: https://github.com/mydana/CircuitPython_DMX_Transmitter
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

# Setup the tx state machine environment.
dmx_state_machine = rp2pio.StateMachine(
    program=dmx_tx_program.assembled,
    frequency=1_000_000,
    first_out_pin=dmx_out_pin,
    out_pin_count=1,
    initial_out_pin_state=1,
    first_sideset_pin=dmx_timing_pin,
    sideset_pin_count=3,
    initial_sideset_pin_state=7,
    exclusive_pin_use=True,
    pull_threshold=16,
    auto_pull=True,
    out_shift_right=True
)

dmx_state_machine.background_write(loop=memoryview(dmx_values))

# DMX profiles
dmx_profile_base = 0 # Start at groups 0-4
dmx_max_midi_profiles = 20 # 20 Profiles assignable by MIDI
dmx_profile_fixed0 = 21 # 1st fixed index
dmx_profile_off = 27 # Off index
dmx_profile_test = 30 # Test (dynamic) index
dmx_max_profiles = 28 # 28 Total Profiles (0-27), 20-26 are fixed colors, 27 is off.
dmx_profiles = [[0 for i in range(4)] for j in range(dmx_max_profiles)]
dmx_profiles[20] = { 255, 0, 0, 0 }    # Profile 20: Red
dmx_profiles[21] = { 0, 255, 0, 0 }    # Profile 21: Green
dmx_profiles[22] = { 0, 0, 255, 0 }    # Profile 22: Blue
dmx_profiles[23] = { 0, 0, 0, 255 }    # Profile 23: White
dmx_profiles[24] = { 255, 150, 0, 0 }  # Profile 24: Yellow
dmx_profiles[25] = { 0, 255, 255, 0 }  # Profile 25: Cyan
dmx_profiles[26] = { 180, 0, 255, 0 }  # Profile 26: Purple
dmx_profiles[27] = { 0, 0, 0, 0 }      # Profile 27: Black

# DMX groups by index
dmx_max_groups = 22 # All (8+4+2+2), Front (8), Back (4), Left (2), Right (2), 16 fixtures, Specials (1) 
dmx_group_all = 0 
dmx_group_index0 = 5 # First group index for fixture
dmx_group_neopixel = 23 # Special group for neopixel, not controlled via DMX.
dmx_group_eyes = 24 # Special group for eyes, not actually controlled here.
dmx_groups = [[0 for i in range(1)] for j in range(dmx_max_groups)]
for j in range(dmx_group_index0, dmx_max_profiles):
    dmx_groups[j] = [j]
dmx_groups[4] = dmx_groups[19] + dmx_groups[20]
dmx_groups[3] = dmx_groups[17] + dmx_groups[18]
dmx_groups[2] = dmx_groups[13] + dmx_groups[14] + dmx_groups[15] + dmx_groups[16]
dmx_groups[1] = dmx_groups[5] + dmx_groups[6] + dmx_groups[7] + dmx_groups[8] + dmx_groups[9] + dmx_groups[10] + dmx_groups[11] + dmx_groups[12]
dmx_groups[0] = dmx_groups[1] + dmx_groups[2] + dmx_groups[3] + dmx_groups[4]

# DMX Adddress mapping
dmx_max_addresses = 17
dmx_addresses = [1, 2, 3, 4, 5, 6, 7, 8, 101, 111, 121, 131, 201, 211, 301, 311, 11]

# DMX values
dmx_value_intensity_off = 8
dmx_value_intensity_max = 134

# set dmx channel values from group
def assignProfile(profile, group, intensity):
    for groupMember in dmx_groups[group]: # Lookup indexes in group
        dmxBaseAddress = dmx_addresses[groupMember] # Get base address for group
        dmx_values[dmx_values_index0 + dmxBaseAddress + 0] = intensity # Intensity
        dmx_values[dmx_values_index0 + dmxBaseAddress + 1] = dmx_profiles[profile][0]  # Red
        dmx_values[dmx_values_index0 + dmxBaseAddress + 2] = dmx_profiles[profile][1]  # Green
        dmx_values[dmx_values_index0 + dmxBaseAddress + 3] = dmx_profiles[profile][2]  # Blue
        dmx_values[dmx_values_index0 + dmxBaseAddress + 4] = dmx_profiles[profile][3]  # White

# Turns off all lights
assignProfile(dmx_profile_off, dmx_group_all, 0)

# Loop
while True:

    #  receive MIDI input
    msg=midi_uart.receive()

    #  if the input is a recognized message...
    if msg is not None:
        if isinstance(msg, ControlChange):
            # Map the first 80 CC messages to DMX profiles 0-19
            print("CC: ", msg.control, "Value:", msg.value)
            profilesIndex = msg.control / 4
            controlIndex = msg.control % 4
            if profilesIndex >= 0 and profilesIndex < dmx_max_midi_profiles:
                dmx_profiles[profilesIndex][controlIndex] = 0 if msg.value == 0 else msg.value + dmx_value_intensity_off
                print("DMX Profile ", profilesIndex, " Control ", controlIndex, " Value: ", dmx_profiles[profilesIndex][controlIndex])

        if isinstance(msg, ProgramChange):
            # Map the program change to a DMX profile base
            # PC controls dmx_profile_base, notes PC 0-5 (6 ranges of 5 groups = 30 groups)
            dmx_profile_base = msg.program * 5
            print("DMX Profile Base ", dmx_profile_base)

        if isinstance(msg, NoteOn) and msg.velocity != 0:
            # Map the not to a DMX group/profile pairing
            # Each note in a 2 octive ranges is mapped to a group number.
            # 5 ranges of 24 groups each = profiles 0-4 + base
            profileOffset = msg.note / 24
            profileIndex = dmx_profile_base + profileOffset
            groupIndex = msg.note % 24
            print("noteOn: ", msg.note, "vel:", msg.velocity)

            if groupIndex >= 0 and groupIndex < dmx_max_groups and profileIndex >= 0 and profileIndex < dmx_max_profiles:
                assignProfile(profileIndex, groupIndex, msg.velocity + dmx_value_intensity_off)
                print("DMX Profile ", profileIndex, " Group ", groupIndex, " Value: ", msg.velocity + dmx_value_intensity_off)

            if (groupIndex == dmx_group_neopixel and profileIndex >= 0 and profileIndex < dmx_max_profiles):
                intensityFactor = msg.velocity
                pixels.show([dmx_profiles[profileIndex][0] * intensityFactor // 127,
                             dmx_profiles[profileIndex][1] * intensityFactor // 127,
                             dmx_profiles[profileIndex][2] * intensityFactor // 127])
                pixels.show()
                print("Neopixel Profile ", profileIndex, " Value: ", msg.velocity + dmx_value_intensity_off)

    # Send test output
    if (dmx_profile_base == dmx_profile_test):
        time.sleep(0.5)
        groupIndex = dmx_test_counter / 4
        profileIndex = dmx_profile_fixed0 + (dmx_test_counter % 4)
        print("DMX Test ", dmx_test_counter, " Group ", groupIndex, " Profile: ", profileIndex)

        for group in range(dmx_max_groups):
            assignProfile(dmx_profile_off, dmx_group_index0 + group, dmx_value_intensity_off)
        if (groupIndex >= 0 and groupIndex < dmx_max_groups and profileIndex >= 0 and profileIndex < dmx_max_profiles):
            assignProfile(profileIndex, groupIndex, dmx_value_intensity_max)

        if (groupIndex == dmx_group_neopixel and profileIndex >= 0 and profileIndex < pixel_count):
            pixels.file([dmx_profiles[profileIndex][0],
                         dmx_profiles[profileIndex][1],
                         dmx_profiles[profileIndex][2]])
        else:
            pixels.fill([dmx_profiles[dmx_profile_off][0],
                         dmx_profiles[dmx_profile_off][1],
                         dmx_profiles[dmx_profile_off][2]])
        pixels.show()

        dmx_test_counter = dmx_test_counter + 1
        if (dmx_test_counter >= (dmx_group_neopixel * 4)):
            dmx_test_counter = 0
