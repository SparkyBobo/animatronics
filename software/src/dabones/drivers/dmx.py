"""
DaBones

DMX output driver.

Copyright (c) 2026 Sparky Bobo
"""

import board
import digitalio
import array
import rp2pio
import adafruit_pioasm

# DMX Configuration Constants
DMX_CHANNELS = 512
DMX_VALUES_INDEX0 = 5  # First channel index in dmx_values array

import logging
logger = logging.getLogger(__name__)

# A DMX driver
class DMXDriver:
    """DMX output driver."""

    def __init__(self, mode_pin=None, out_pin=None, timing_pin=None) -> None:
        """
        Initialize DMXDriver.

        Args:
            mode_pin: GPIO pin for DMX mode control (default: board.GP7)
            out_pin: GPIO pin for DMX data output (default: board.GP8)
            timing_pin: GPIO pin for timing control (default: board.GP4)
        """
        # Set default pins if not provided
        self.mode_pin_num = mode_pin or board.GP7
        self.out_pin = out_pin or board.GP8
        self.timing_pin = timing_pin or board.GP4
        
        # Initialize mode pin
        self.dmx_mode_pin = digitalio.DigitalInOut(self.mode_pin_num)
        self.dmx_mode_pin.direction = digitalio.Direction.OUTPUT
        self.dmx_mode_pin.value = True  # Set to transmit
        
        # Initialize DMX values buffer
        # Array structure: [MBB, BRK, MAB, channel_count, start_code, ch1_data, ch2_data, ...]
        self.dmx_values = array.array("L", (0 for _ in range(DMX_CHANNELS + 5)))
        
        # Setup tx timings - See https://support.etcconnect.com/ETC/FAQ/DMX_Speed
        # These timings are close to the Eos family of products "medium" speed.
        self.dmx_values[0] = 30            # Word 0: Length of MARK BEFORE BREAK in microseconds (8us min)
        self.dmx_values[1] = 142           # Word 1: Length of SPACE FOR BREAK in microseconds (92us min)
        self.dmx_values[2] = 128           # Word 2: Length of MARK AFTER BREAK in microseconds (12us min)
        self.dmx_values[3] = DMX_CHANNELS  # Word 3: Number of channels to send (1-512) + (1 for start code)
        self.dmx_values[4] = 0             # Word 4: Start Code data byte (usually 0)
        
        # Initialize DMX state machine with PIO program
        self._init_state_machine()
        
        logger.info("DMXDriver initialized.")
    
    def _init_state_machine(self):
        """Initialize the DMX-512 PIO state machine"""
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
        self.dmx_state_machine = rp2pio.StateMachine(
            program=dmx_tx_program.assembled,
            frequency=1_000_000,
            first_out_pin=self.out_pin,
            out_pin_count=1,
            initial_out_pin_state=1,
            first_sideset_pin=self.timing_pin,
            sideset_pin_count=3,
            initial_sideset_pin_state=7,
            exclusive_pin_use=True,
            pull_threshold=16,
            auto_pull=True,
            out_shift_right=True
        )
        
        # Start background transmission
        self.dmx_state_machine.background_write(loop=memoryview(self.dmx_values))
    
    def set_dmx_level(self, channel, value):
        """
        Set a single DMX channel level
        
        Args:
            channel: DMX channel number (1-512)
            value: Channel value (0-255)
        """
        if channel >= 1 and channel <= DMX_CHANNELS:
            self.dmx_values[DMX_VALUES_INDEX0 + channel - 1] = value
    
    def get_dmx_level(self, channel):
        """
        Get a single DMX channel level
        
        Args:
            channel: DMX channel number (1-512)
            
        Returns:
            Channel value (0-255)
        """
        if channel >= 1 and channel <= DMX_CHANNELS:
            return self.dmx_values[DMX_VALUES_INDEX0 + channel - 1]
        return 0

    def set_dmx_levels(self, channel_value_pairs):
        """
        Update multiple DMX channels in one call.
        
        Args:
            channel_value_pairs: iterable of (channel, value) tuples where
                channel is 1-512 and value is 0-255. Invalid entries are skipped.
        """
        for channel, value in channel_value_pairs:
            if 1 <= channel <= DMX_CHANNELS:
                # clamp value between 0 and 255 just in case
                val = value
                if val < 0:
                    val = 0
                elif val > 255:
                    val = 255
                self.dmx_values[DMX_VALUES_INDEX0 + channel - 1] = val
    
    def all_off(self):
        """Turn off all DMX channels"""
        for i in range(DMX_CHANNELS):
            self.dmx_values[DMX_VALUES_INDEX0 + i] = 0
    
    def get_values(self):
        """
        Get the DMX channel values array
        
        Returns:
            The last DMX_CHANNELS elements of dmx_values (the channel data)
        """
        return self.dmx_values[-DMX_CHANNELS:]


