"""
DaBones

Streamdeck mini driver.

The Mini family (PID 0x0063, 0x0090, 0x00B3, 0x00B8) uses a DIFFERENT
protocol from the main Stream Deck family (Classic/XL/Neo/Plus). Do not
reuse report IDs or structures from the main-protocol driver.

Protocol reference: https://docs.elgato.com/streamdeck/hid/mini

Copyright (c) 2026 Sparky Bobo
"""

import array
import time

import usb.core
import adafruit_usb_host_descriptors as descriptors

#import logging
#logger = logging.getLogger(__name__)

VENDOR_ID = 0x0FD9
PRODUCT_ID = 0x0063  # Mini. Use 0x0090 / 0x00B3 / 0x00B8 for other Mini variants

HID_SET_REPORT = 0x09
HID_GET_REPORT = 0x01
REPORT_TYPE_FEATURE = 0x03

DESC_INTERFACE = 0x04
DESC_ENDPOINT = 0x05
DIR_IN = 0x80

# Getter feature report IDs (Mini protocol -- do not confuse with main protocol)
REPORT_ID_FW_LD = 0xA0
REPORT_ID_FW_AP2 = 0xA1  # primary firmware
REPORT_ID_FW_AP1 = 0xA2  # backup firmware
REPORT_ID_SERIAL = 0x03
REPORT_ID_SLEEP_DURATION = 0xA3

FEATURE_REPORT_SIZE = 32

# A method to find HID endpoints.
def find_hid_endpoints(device):
    config = descriptors.get_configuration_descriptor(device, 0)

    interface_number = None
    ep_in = None
    ep_out = None
    ep_in_max_packet = None
    ep_out_max_packet = None

    i = 0
    in_target_interface = False
    while i < len(config):
        length = config[i]
        desc_type = config[i + 1]

        if desc_type == DESC_INTERFACE:
            interface_number = config[i + 2]
            in_target_interface = True

        elif desc_type == DESC_ENDPOINT and in_target_interface:
            addr = config[i + 2]
            max_packet = config[i + 4] | (config[i + 5] << 8)
            if addr & DIR_IN:
                if ep_in is None:
                    ep_in = addr
                    ep_in_max_packet = max_packet
            else:
                if ep_out is None:
                    ep_out = addr
                    ep_out_max_packet = max_packet

        i += length

    return interface_number, ep_in, ep_out, ep_in_max_packet, ep_out_max_packet

# A StreamDeck(Mini) driver.
class StreamDeckMini:
    """StreamDeckMini driver."""

    def __init__(self) -> None:
        """Initialize Streamdeck driver."""
        dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if dev is None:
            raise RuntimeError("Stream Deck Mini not found — check USB host wiring/power")
        self.dev = dev

        self.interface_number, self.ep_in, self.ep_out, self.ep_in_max_packet, self.ep_out_max_packet = (
            find_hid_endpoints(dev)
        )
        if self.interface_number is None or self.ep_in is None:
            raise RuntimeError("Could not locate HID interface/endpoints")

        print(
            "HID interface", self.interface_number,
            "ep_in", hex(self.ep_in), "max_packet", self.ep_in_max_packet,
            "ep_out", hex(self.ep_out) if self.ep_out is not None else None,
            "max_packet", self.ep_out_max_packet,
        )

        if dev.is_kernel_driver_active(self.interface_number):
            dev.detach_kernel_driver(self.interface_number)

        dev.set_configuration()

        self._in_buf = array.array("B", [0] * 65)  # fixed 65-byte input report

    # --- Feature report helpers --------------------------------------
    def _get_feature(self, report_id):
        """Sends HID GET_FEATURE_REPORT and returns the 32-byte response."""
        buf = array.array("B", [0] * FEATURE_REPORT_SIZE)
        self.dev.ctrl_transfer(
            0xA1,  # device->host, class, interface
            HID_GET_REPORT,
            (REPORT_TYPE_FEATURE << 8) | report_id,
            self.interface_number,
            buf,
        )
        return buf

    def _set_feature(self, payload):
        buf = bytearray(FEATURE_REPORT_SIZE)
        buf[: len(payload)] = payload
        self.dev.ctrl_transfer(
            0x21,  # host->device, class, interface
            HID_SET_REPORT,
            (REPORT_TYPE_FEATURE << 8) | buf[0],
            self.interface_number,
            buf,
        )

    # --- Buttons ---------------------------------------------------
    def poll_buttons(self, debug=False):
        """Reads the fixed 65-byte input report. Returns a 6-byte
        bytearray of key states (0x00 released, 0x01 pressed), or
        None on timeout / no event."""
        # Clear stale bytes so a short/partial read can't leak
        # leftover data from a previous report into this one.
        for i in range(len(self._in_buf)):
            self._in_buf[i] = 0

        try:
            n = self.dev.read(self.ep_in, self._in_buf, timeout=10)
        except usb.core.USBTimeoutError:
            return None
        except usb.core.USBError:
            return None

        if debug:
            print("n =", n, "raw =", list(self._in_buf[:17]))

        if n < 7 or self._in_buf[0] != 0x01:
            return None

        # +0x00 report id, +0x01 payload[64], only first 6 bytes used
        return bytes(self._in_buf[1:7])

    def poll_buttons_debounced(self, debounce_ms=30, debug=False):
        """Like poll_buttons(), but ignores any state change that
        arrives within debounce_ms of the previously accepted change
        (filters contact bounce). The Mini only sends a report when
        state actually changes, so this uses a lockout window rather
        than requiring repeated identical samples."""
        now = time.monotonic()
        raw = self.poll_buttons(debug=debug)

        if raw is None:
            return None

        if debug:
            print("raw event:", list(raw))

        if not hasattr(self, "_confirmed_state"):
            self._confirmed_state = raw
            self._last_change = now
            return raw  # first real event -- accept it

        if raw == self._confirmed_state:
            if debug:
                print("  -> rejected: duplicate of confirmed state")
            return None  # duplicate report, no actual change

        if (now - self._last_change) < (debounce_ms / 1000):
            if debug:
                print("  -> rejected: inside lockout window")
            return None  # too soon after last accepted change -- bounce

        self._confirmed_state = raw
        self._last_change = now
        return raw

    # --- Getters -------------------------------------------------------
    def get_firmware_version(self, which="AP2"):
        """which: 'LD', 'AP2' (primary), or 'AP1' (backup)."""
        report_id = {
            "LD": REPORT_ID_FW_LD,
            "AP2": REPORT_ID_FW_AP2,
            "AP1": REPORT_ID_FW_AP1,
        }[which]

        buf = self._get_feature(report_id)
        # +0x00 report id, +0x01..0x04 unused, +0x05 ASCII[12]
        raw = bytes(buf[5:5 + 12])
        return raw.split(b"\x00", 1)[0].decode("ascii", "replace")

    def get_serial_number(self):
        buf = self._get_feature(REPORT_ID_SERIAL)
        # length isn't fixed; scan up to end of buffer for the ASCII string
        raw = bytes(buf[5:])
        return raw.split(b"\x00", 1)[0].decode("ascii", "replace")

    def get_sleep_mode_duration(self):
        buf = self._get_feature(REPORT_ID_SLEEP_DURATION)
        data_length = buf[1]
        duration = buf[2] | (buf[3] << 8) | (buf[4] << 16) | (buf[5] << 24)
        return duration if data_length else 0

    # --- Setters used elsewhere in this file's protocol (for reference) -
    def set_brightness(self, percent):
        percent = max(0, min(100, percent))
        self._set_feature(bytes([0x05, 0x55, 0xAA, 0xD1, 0x01, percent]))

    def show_logo(self):
        self._set_feature(bytes([0x0B, 0x63, 0x00]))

    # --- Image upload (interrupt/bulk OUT, chunked) ------------------
    # Output reports on the Mini are a FIXED size of 1024 bytes, with a
    # 16-byte header (offset 0x00-0x0F), leaving 1008 bytes of payload
    # per chunk. This differs from the main-protocol driver's 8-byte
    # header / variable chunk size.
    OUTPUT_REPORT_SIZE = 1024
    HEADER_SIZE = 0x10
    CHUNK_PAYLOAD_SIZE = OUTPUT_REPORT_SIZE - HEADER_SIZE  # 1008

    def set_key_image(self, key_index, bmp_bytes, show=True):
        """Uploads a pre-encoded BMP (80x80, rotated 90deg clockwise)
        to a single key's memory bank.

        bmp_bytes: raw BMP file bytes, already rotated/sized correctly.
        show: if True, displays immediately on the given key. If False,
              stores into the memory bank without displaying (matches
              the 'Show Image flag' in the protocol).
        """
        if self.ep_out is None:
            raise RuntimeError("No OUT endpoint available for image upload")

        offset = 0
        chunk_index = 0
        total = len(bmp_bytes)
        show_flag = 0x01 if show else 0x00

        while offset < total or total == 0:
            chunk = bmp_bytes[offset: offset + self.CHUNK_PAYLOAD_SIZE]

            packet = bytearray(self.OUTPUT_REPORT_SIZE)
            packet[0] = 0x02          # Report ID
            packet[1] = 0x01          # Command: Upload Data to Image Memory Bank
            packet[2] = chunk_index & 0xFF
            packet[3] = 0x00          # Reserved
            packet[4] = show_flag
            packet[5] = key_index
            # bytes 6-15 reserved, already zero from bytearray init
            packet[self.HEADER_SIZE:self.HEADER_SIZE + len(chunk)] = chunk

            self.dev.write(self.ep_out, packet)

            offset += len(chunk)
            chunk_index += 1
            if offset >= total:
                break
