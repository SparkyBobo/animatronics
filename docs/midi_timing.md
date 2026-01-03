# MIDI Playback Timing

## Overview

The DaBones use a combination of System Common and System Real-Time messages with MIDI channel 0 for
playback of locally stored MIDI files. The timing related messages and file sections include:

## Messages

Status|Data Byte(s)|Description
------|------------|-----------
11110010|0lllllll 0mmmmmmm|Song Position Pointer. This is an internal 14-bit register that holds the number of MIDI beats (1 beat = six MIDI clocks) since the start of the song. l is the LSB, m the MSB.
11111000||Timing Clock. Sent 24 times per quarter note when synchronisation is required.
11111010||Start. Start the current sequence playing. (This message will be followed with Timing Clocks).

### Song Position Pointer.

This is an internal 14-bit register that holds the number of MIDI beats (1 beat = six MIDI clocks) since the start of the song. l is the LSB, m the MSB: 0lllllll 0mmmmmmm.

The controller may use this message to set the song element sequencers to a fixed point in the song. This register
is reset to 0 when a new song is played.

### Timing Clock

Sent 24 times per quarter note for real-time playback. Can be sent at a slower rate to step through the
events in the MIDI file.

### Start

Start the current sequence playing. (This message will be followed with Timing Clocks). This will reset the song
position register to 0.

## Files

File section|Value|Comment
------------|-----|-----------
Header|division|ticks per quarter-note
Track 0|time signature|time signature
Track 0|tempo|microseconds per MIDI quarter-note

### Division

The division specifies the meaning of the delta-times. It uses ticks per quarter-note:

bit 15|bits 14 thru 0
-----|-----
0|ticks per quarter-note

ticks per quarter-note represent the number of delta time "ticks" which make up a quarter-note.
For instance, if division is 96, then a time interval of an eighth-note between two events in the file would be 48.
If not supplied, the default value is 24.

### Tempo

The song tempo in microseconds per MIDI quarter-note, e.g., 07 A1 20 = 500,000 usec/quarter note = 120 beats/minute.

## Calculations

When playing MIDI files locally, the following process describes how timing is controlled.

1. When a file is loaded, the ticks per quarter note, division, and tempo are set based on the contents of the file header and track metadata. Changes to these parameters are not supported. The position is reset to 0.
2. Determine the ticks per timing clock: ticks per timing clock = division / 24. Default is 1.
3. Calculate the expected timing clock interval: timing clock interval = tempo / 24 milliseconds.
4. Calculate the tick rate: ticks per millisecond = ticks per timing clock / timing clock interval.
5. If no timing clocks are received, play using these calculated variables.
6. If timing clocks are received, use them to override the expected timing and recalculate the tick rate.
7. Recalculate the tick rate using actual timing clock intervals: ticks per millisecond = ticks per timing clock / (current clock time - previous clock time).
8. Increment ticks using the last known tick rate. Timing may be inaccurate if intervals change.
9. Evaluate file events for every tick increment.
10. Increment the song position pointer by 1 every 6 MIDI timing clocks.
11. If the song position pointer is adjusted, calculate ticks = song position pointer * ticks per timing clock * 6 and pause playback.

