"""
DaBones

Streamdeck mini driver test.

Copyright (c) 2026 Sparky Bobo
"""

#import time
#from animacy.drivers.streamdeck import StreamDeckMini

# def test_streamdeck_get_info():
#     deck = StreamDeckMini()
#     print("Serial:", deck.get_serial_number())
#     print("Firmware AP2 (primary):", deck.get_firmware_version("AP2"))
#     print("Firmware AP1 (backup):", deck.get_firmware_version("AP1"))
#     print("Firmware LD:", deck.get_firmware_version("LD"))
#     print("Sleep duration (s):", deck.get_sleep_mode_duration())

#     deck.set_brightness(60)

#     print("Polling buttons — press Ctrl-C to stop")
#     last_state = bytes(6)  # all released
#     while last_state[5] == False:
#         state = deck.poll_buttons_debounced(debounce_ms=30, debug=True)
#         if state is not None:
#             for i in range(6):
#                 if state[i] != last_state[i]:
#                     print("Key", i, "pressed" if state[i] else "released")
#             last_state = state
#         time.sleep(0.01)

