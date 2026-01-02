# MIDI Playback

## Overview 

The DaBones use a combination of System Common and System Real-Time messages with MIDI channel 0 for
playback of locally stored MIDI files.

For details regarding files, see [MIDI Files](./midi_file.md).
For details regarding file transfers, see [MIDI File Transfers](./midi_file_transfer.md).

## Messages 

When used in with MIDI files, MIDI messages can signal start, stop and timing information for a song.
These messages include:

Status|Data Byte(s)|Description
------|------------|-----------
11110010|0lllllll 0mmmmmmm|Song Position Pointer. This is an internal 14 bit register that holds the number of MIDI beats (1 beat= six MIDI clocks) since the start of the song. l is the LSB, m the MSB.
11110011|0sssssss|Song Select. The Song Select specifies which sequence or song is to be played.
11110110||Tune Request. Upon receiving a Tune Request, song elements should "tune" their instruments.
11111000||Timing Clock. Sent 24 times per quarter note when synchronisation is required.
11111010||Start. Start the current sequence playing. (This message will be followed with Timing Clocks).
11111011||Continue. Continue at the point the sequence was Stopped.
11111100||Stop. Stop the current sequence.
11111110||Active Sensing. Use of this message is required. When initially sent, the receiver will expect to receive another Active Sensing message each 300ms (max), or it will be assume that the connection has been terminated. At termination, the receiver will turn off all voices and return to normal (non-active sensing) operation.
11110000|01111111 01111111 00000004 00000001 vvvvvvvv vvvvvvvv|Master volume. Sets the master volume, (vvvvvvvv vvvvvvvv) is the volume level 0-65535, lsb first.
11110000|01111111 01111111 10111111 00000001 ...|Open File
11110000|01111111 01111111 10111111 00000004 ...|Close File
11111111||Reset. Reset all receivers in the system to power-up status.

### Song Position Pointer.

This is an internal 14 bit register that holds the number of MIDI beats (1 beat= six MIDI clocks) since the start of the song. l is the LSB, m the MSB: 0lllllll 0mmmmmmm.

The controller may use this message to set the song element sequencers to a fixed point in the song. This register
is reset to 0 when a new song is played.

### Song Select

The song Select specifies which sequence or song is to be played. It only works for songs 0-127. For higher
song number use the system exclusive message Open File for file selection. 

### Tune Request

Upon receiving a Tune Request, all song elements "tune" their instruments. This request will trigger the song element
to excercise its functionality in a "power up" sequence to visual song all elements working. The tune request
will last 10 seconds during which the song element will continue to display its pattern.

### Timing Clock

Sent 24 times per quarter note for real time playback. Can be sent at a slower rate to stepping through the
events in the MIDI file.

### Start

Start the current song playing. (This message will be followed with Timing Clocks). This will reset the song
position register to 0.

### Continue

Continue at the point the sequence was Stopped. Operates like a pause button on a cassette deck.

### Stop

Stop the current sequence. This will not reset the song position register to 0.

### Active Sensing

Use of this message is optional. When initially sent, the receiver will expect to receive another Active Sensing message each 300ms (max), or it will be assume that the connection has been terminated. At termination, the receiver will turn off all voices and return to normal (non-active sensing) operation.

### Master Volume

Sets the master volume, (vvvvvvvv vvvvvvvv) is the volume level 0-65535, lsb first. This is a real-time universal system exclusive event and belongs to the playback category.

### Open File

This message specifies the type and location of a MIDI file so it can be loaded. It does not cause the
song to play. This can be used in place of Song Select messages which the song number exceeds 127 or
for specifying a non-standard file name. This is a non-real-time universal system exclusive event and belongs to the playback category.

The command includes the following data bytes:

Data|Comment
----|-------
0ccccccc 0ccccccc|Two 7-bit byte command context. Use 00000000 00000000.
0lllllll 0lllllll|Two 7-bit byte combined byte count of type and name, lsb first.
0ttttttt 0ttttttt 0ttttttt 0ttttttt|Four 7-bit byte type. Use 'MIDI'.
0nnnnnnn ...|Variable length, NULL terminated, 7-bit ASCII byte file name. Maximum length including terminator is 261 bytes.

If the name specified is a partial match for a single file, that file is opened. For instance, if the
file name is "0006_" and a single file such as "0006_ome_text.mid" exists, it is opened.

### Close File

This message closes an open file and deallocates any memory allocated for the file's contents. This is a non-real-time universal system exclusive event and belongs to the playback category.

The command includes the following data bytes:

Data|Comment
----|-------
0ccccccc 0ccccccc|Two 7-bit byte command context. Use 00000000 00000000.

### Reset.

Reset all receivers in the system to power-up status. Upon reset, all song elements will perform a "tune" operation
as described in Tune Request.



