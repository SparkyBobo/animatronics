# MIDI Playback

## Overview

The DaBones use a combination of System Common and System Real-Time messages with MIDI channel 0 for
playback of locally stored MIDI files. The timing related messages and file sections include:

## Messages

Status|Data Byte(s)|Description
------|------------|-----------
11110010|0lllllll 0mmmmmmm|Song Position Pointer. This is an internal 14 bit register that holds the number of MIDI beats (1 beat= six MIDI clocks) since the start of the song. l is the LSB, m the MSB.
11111000||Timing Clock. Sent 24 times per quarter note when synchronisation is required.
11111010||Start. Start the current sequence playing. (This message will be followed with Timing Clocks).

### Song Position Pointer.

This is an internal 14 bit register that holds the number of MIDI beats (1 beat= six MIDI clocks) since the start of the song. l is the LSB, m the MSB: 0lllllll 0mmmmmmm.

The controller may use this message to set the song element sequencers to a fixed point in the song. This register
is reset to 0 when a new song is played.

### Timing Clock

Sent 24 times per quarter note for real time playback. Can be sent at a slower rate to stepping through the
events in the MIDI file.

### Start

Start the current song playing. (This message will be followed with Timing Clocks). This will reset the song
position register to 0.

## Files

File section|Value|Comment
------------|-----|-----------
Header|division|ticks per quarter-note
Track 0|time signature|time signature
Track 0|tempo|microseconds per MIDI quarter-note

### Division

The third word, division, specifies the meaning of the delta-times. It uses ticks per quarter-note:

bit 15|bits 14 thru 0
-----|-----
0|ticks per quarter-note

ticks per quarter-note represent the number of delta time "ticks" which make up a quarter-note.
For instance, if division is 96, then a time interval of an eighth-note between two events in the file would be 48.

### Time Signature

The time signature is expressed as four numbers. nn and dd represent the numerator and denominator of the time signature as it would be notated. The denominator is a negative power of two: 2 represents a quarter-note, 3 represents an eighth-note, etc. The cc parameter expresses the number of MIDI clocks in a metronome click. The bb parameter expresses the number of notated 32nd-notes in a MIDI quarter-note (24 MIDI clocks). This was added because there are already multiple programs which allow a user to specify that what MIDI thinks of as a quarter-note (24 clocks) is to be
notated as, or related to in terms of, something else.

e.g., 04 02 24 08 = 4/4 time; 24 MIDI clocks/click, 8 32nd notes/ 24 MIDI clocks (24 MIDI clocks = 1 crotchet = 1 beat)

### Tempo

The song tempo in microseconds per MIDI quarter-note, e.g., 07 A1 20 = 500,000 usec/ quarter note = 120 beats/minute.

## Calculations

When playing MIDI files locally during playback, the following process dewscribes how timing is controlled.


### Song Position Pointer.

This is an internal 14 bit register that holds the number of MIDI beats (1 beat= six MIDI clocks) since the start of the song. l is the LSB, m the MSB: 0lllllll 0mmmmmmm.

