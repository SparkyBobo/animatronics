# MIDI Messages

## Overview

The DaBones use MIDI messages, with one MIDI channels for each "instrument", i.e., character or song element.
The messages can be played live as you would play any other instrument to control the song elements.

The disadvantage of using MIDI messages is that the song element cannot anticipate messages, giving
song elements a less natural representation of the event, i.e., the swing of the drum stick appears
less human and more mechanical. Messages are not used for final playback during a show. Instead,
messages are used to synchronize the show elements during the show.

However, messages are useful during the progrmaming stage. Each song element can respond to the messages
to help show where each song element will be for every moment in the song. While the mechanics may be
unnatural, this is acceptable during programming where it's more important to define the states than
the process of acheiving the state.

## Song Playback

When used in with MIDI files, MIDI messages can signal start, stop and timing information for a song.
These messages include:

Status|Data Byte(s)|Description
------|------------|-----------
11110010|0lllllll 0mmmmmmm|Song Position Pointer. This is an internal 14 bit register that holds the number of MIDI beats (1 beat= six MIDI clocks) since the start of the song. l is the LSB, m the MSB.
11110011|0sssssss|song Select. The song Select specifies which sequence or song  is to be played.
11110110||Tune Request. Upon receiving a Tune Request, all analog synthesisers should tune their oscillators.
11111000||Timing Clock. Sent 24 times per quarter note when synchronisation is required.
11111010||Start. Start the current sequence playing. (This message will be followed with Timing Clocks).
11111011||Continue. Continue at the point the sequence was Stopped.
11111100||Stop. Stop the current sequence.
11111110||Active Sensing. Use of this message is required. When initially sent, the receiver will expect to receive another Active Sensing message each 300ms (max), or it will be assume that the connection has been terminated. At termination, the receiver will turn off all voices and return to normal (non-active sensing) operation.
11111111||Reset. Reset all receivers in the system to power-up status.
11110000||System Exclusive. System exclusive messages are used to transfer MIDI files between song elements and select files for playback. For details regarding file transfers, see [MIDI File Transfers](./midi_file_transfer.md).

For a details regarding playback, see [MIDI Playback](./midi_playback.md).

## Song Element Control

MIDI messages, with one MIDI channels for each "instrument", i.e., character or song element,
the messages can be played live as you would play any other instrument to control the song elements.
Much like a live MIDI stream might be used to control instruments. In this mode, each song element will
respond to it's MIDI channel and messages the same as it would during playback, except the element is not
able to anticipate the next event, e.g., the swing of the drum stick appears more mechanical and less human.

Status|Data Byte(s)|Description
------|------------|-----------
1000nnnn|0kkkkkkk 0vvvvvvv|Note Off event. This message is sent when a note is released (ended). (kkkkkkk) is the key (note) number. (vvvvvvv) is the velocity.
1001nnnn|0kkkkkkk 0vvvvvvv|Note On event. This message is sent when a note is depressed (start). (kkkkkkk) is the key (note) number. (vvvvvvv) is the velocity.
1011nnnn|0ccccccc 0vvvvvvv|Control Change. This message is sent when a controller value changes. Controllers include devices such as pedals and levers. Certain controller numbers are reserved for specific purposes. See Channel Mode Messages. (ccccccc) is the controller number. (vvvvvvv) is the new value.
1100nnnn|0ppppppp|Program Change. This message sent when the patch number changes. (ppppppp) is the new program number.
1110nnnn|0lllllll 0mmmmmmm|Pitch Wheel Change. This message is sent to indicate a change in the pitch wheel. The pitch wheel is measured by a fourteen bit value. Centre (no pitch change) is 2000H. Sensitivity is a function of the transmitter. (lllllll) are the least significant 7 bits. (mmmmmmm) are the most significant 7 bits.

For a list of MIDI channels, see [MIDI Channels](./midi_channel.md)
For a list of MIDI notes, controls, and programs, see [MIDI Notes, Controls, and Programs](./midi_notes.md)
