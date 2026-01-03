# MIDI Notes, Controls, and Programs

## Overview

Status|Data Byte(s)|Description
------|------------|-----------
1000nnnn|0kkkkkkk 0vvvvvvv|Note Off event. This message is sent when a note is released (ended). (kkkkkkk) is the key (note) number. (vvvvvvv) is the velocity.
1001nnnn|0kkkkkkk 0vvvvvvv|Note On event. This message is sent when a note is depressed (start). (kkkkkkk) is the key (note) number. (vvvvvvv) is the velocity.
1011nnnn|0ccccccc 0vvvvvvv|Control Change. This message is sent when a controller value changes. Controllers include devices such as pedals and levers. Certain controller numbers are reserved for specific purposes. See Channel Mode Messages. (ccccccc) is the controller number. (vvvvvvv) is the new value.
1100nnnn|0ppppppp|Program Change. This message is sent when the patch number changes. (ppppppp) is the new program number.
1110nnnn|0lllllll 0mmmmmmm|Pitch Wheel Change. This message is sent to indicate a change in the pitch wheel. The pitch wheel is measured by a fourteen-bit value. Center (no pitch change) is 2000H. Sensitivity is a function of the transmitter. (lllllll) are the least significant 7 bits. (mmmmmmm) are the most significant 7 bits.

For a list of MIDI channels, see [MIDI Channels](./midi_channel.md)

## Notes
## Controls
## Programs

