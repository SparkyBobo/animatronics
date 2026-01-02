# MIDI Files

## Overview 

The DaBones use MIDI format 1 with multiple tracks, one for each "instrument", i.e., character or song element.
A file may contain all song elements or a single element. The file can be transfered to a song element and played
back upon request.

The advantage of using MIDI files is that the song elements can anticipate events from the file, giving
song elements a more natural representation of the event, i.e., the swing of the drum stick appears
more human and less mechanical. Files are used for final playback during a song.

## File Name

DaBones MIDI file name are standardized to provide organized but human readable names making it easy
to load a file and understand what it contains fron the file name.

File names start with the unique sequence number for the song followed by an underscore. For example, 
song `00 06` would start with "0006_". This makes it easy for the sequence to load the file for a given
song by searching the file list of a song number.

Additionally, files can be transferred between song elements using MIDI system exclusive events. The common
use case is to load the master song file to all elements from a controlled. For details regarding file transfers, see [MIDI File Transfers](./midi_file_transfer.md).

## Header

Format 1 header chunk:

Bytes|Value
-----|-----
4D 54 68 64|MThd
00 00 00 06|chunk length
00 01	   |format 1
00 04	   |number tracks
00 60	   |division, 96 ticks per quarter note

### Division

The third word, division, specifies the meaning of the delta-times. It uses ticks per quarter-note:

bit 15|bits 14 thru 0
-----|-----
0|ticks per quarter-note

ticks per quarter-note represent the number of delta time "ticks" which make up a quarter-note. 
For instance, if division is 96, then a time interval of an eighth-note between two events in the file would be 48.

## Track 0: Metadata

Track 0 contains the metadata for the file as a track chunk:

Bytes|Value
-----|-----
4D 54 72 6B|MTrk
00 00 xx xx|chunk length

Delta-Time|Event|Comments
-----|-----|-----
00|FF 00 02 xx xx|sequence number
00|FF 03 xx xx xx|sequence name
00|FF 04 04 6d 65 74 61|instrument name, "meta" for track 0
00|FF 20 01 00|MIDI channel prefix, 00000000 for track 0
00|FF 58 04 04 02 18 08|time signature
00|FF 51 03 07 A1 20|tempo
00|FF 2F 00|end of track

### FF 00 02: sequence number

A unique sequence number for the song, e.g., `00 01`

### FF 03 len text: sequence name

The name of the sequence, e.g., 'Skeleton Sam'

### FF 04 len text: instrument name

A description of the type of instrumentation to be used in that track, e.g., "meta" for track 0. Informational only.

### FF 20 01 cc MIDI channel prefix

The MIDI channel for the track, e.g., 00000000 for track 0.

For a list of MIDI channels, see [MIDI Channels](./midi_channel.md)

### FF 58 04 nn dd cc bb: time signature

The time signature is expressed as four numbers. nn and dd represent the numerator and denominator of the time signature as it would be notated. The denominator is a negative power of two: 2 represents a quarter-note, 3 represents an eighth-note, etc. The cc parameter expresses the number of MIDI clocks in a metronome click. The bb parameter expresses the number of notated 32nd-notes in a MIDI quarter-note (24 MIDI clocks). This was added because there are already multiple programs which allow a user to specify that what MIDI thinks of as a quarter-note (24 clocks) is to be 
notated as, or related to in terms of, something else.

e.g., 04 02 24 08 = 4/4 time; 24 MIDI clocks/click, 8 32nd notes/ 24 MIDI clocks (24 MIDI clocks = 1 crotchet = 1 beat)

### FF 51 03 tttttt: tempo

The song tempo in microseconds per MIDI quarter-note, e.g., 07 A1 20 = 500,000 usec/ quarter note = 120 beats/minute.

### FF 2F 00 End of Track

This event is not optional. It is included so that an exact ending point may be specified for the track, so that an exact length is defined, which is necessary for tracks which are looped or concatenated.

## Track 1-n: Song element

Tracks 1-n are the different song elements. They are composed of events to trigger each element to correspond to the
sequence being played, e.g., vocal events for a singer:

Bytes|Value
-----|-----
4D 54 72 6B|MTrk
00 00 xx xx|chunk length

Delta-Time|Event|Comments
-----|-----|-----
00|FF 04 04 6d 65 74 61|instrument name, e.g., "joey" or "lights"
00|FF 20 01 cc|MIDI channel prefix.
xx|xx xx xx|MIDI events, i.e., triggers
00|FF 2F 00|end of track

### FF 04 len text: instrument name

A description of the song element for the tracktrack, e.g., "joey" or "lights". Informational only.

### FF 20 01 cc MIDI channel prefix

The MIDI channel for the track. This value, not the name, is used to determine which track
applies to which song element.

For a list of MIDI channels, see [MIDI Channels](./midi_channel.md)

### MIDI events

For a list of MIDI events such as notes, controls, and programs, see [MIDI Notes, Controls, and Programs](./midi_notes.md)

### FF 2F 00 End of Track
This event is not optional. It is included so that an exact ending point may be specified for the track, so that an exact length is defined, which is necessary for tracks which are looped or concatenated.

## Example File

The following is a sequence of bytes that represent a sonmg with a male singer and electric guitar playing
at 96 ticks per quarter note, 4/4 time; 24 MIDI clocks/click, 8 32nd notes/ 24 MIDI clocks, 500,000 usec/ quarter note = 120 beats/minute which play for 4 beats.

Bytes|Value
-----|-----
4D 54 68 64|MThd
00 00 00 06|chunk length
00 01	   |format 1
00 03	   |3 tracks
00 60	   |division, 96 ticks per quarter note
4D 54 72 6B|MTrk, track 0
00 00 00 10|track length (16)
00 FF 00 02 00 00|sequence number, 0.
00 FF 03 74 65 73 74|sequence name, "test"
00 FF 04 04 6d 65 74 61|instrument name, "meta" for track 0
00 FF 20 01 00|MIDI channel prefix, 00 for track 0
00 FF 58 04 04 02 18 08|time signature
00 FF 51 03 07 A1 20|tempo
00 FF 2F 00|end of track
4D 54 72 6B|MTrk, track 1
00 00 00 10|chunk length (16)
00 FF 04 04 6a 6f 65 79|instrument name, "joey"
00 FF 20 01 01|MIDI channel prefix, 00000001 for male singer.
00 C0 05|??
81 40 90 4C 20|??
81 40 4C 00|Running status: note on, vel=0
00 FF 2F 00|end of track
4D 54 72 6B|MTrk, track 2
00 00 00 10|chunk length (16)
00 FF 04 04 73 6c 61 73 68|instrument name, "slash"
00 FF 20 01 06|MIDI channel prefix, 06 for electric guitar.
00 C0 05|??
81 40 90 4C 20|??
81 40 4C 00|Running status: note on, vel=0
00 FF 2F 00|end of track
