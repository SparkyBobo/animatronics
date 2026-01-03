# MIDI

## Overview

The DaBones use MIDI to synchronize and play song elements. MIDI was chosen because:

1. MIDI seemed like a natural fit for controlling things that are based on music
2. MIDI is cheap to implement from a software and hardware perspective
3. MIDI works well over relatively short links, and the song elements are closely grouped together
4. MIDI has a robust protocol definition capable of handling all aspects of the required communication
5. MIDI interoperates with Digital Audio Workstations (DAWs) well so the DAW can become the programming surface

The DaBones use MIDI channels to target individual song elements, with one MIDI channel for each "instrument", i.e., character or song element, e.g., lights.
This allows each song element to be targeted individually or as a single group. For a list of MIDI channels, see [MIDI Channels](./midi_channel.md).

The DaBones use MIDI messages to control each song element. The messages can be played live as you would play any other instrument to control the song elements.
The DaBones use System Common and System Real-Time messages with MIDI channel 0 for playback of locally stored MIDI files, and System Exclusive messages to transfer files to all show elements. 

- For a list of MIDI messages, see [MIDI Messages](./midi_messages.md)
- For a list of MIDI notes, controls, and programs, see [MIDI Notes, Controls, and Programs](./midi_notes.md)
- For details regarding playback, see [MIDI Playback](./midi_playback.md).
- For details regarding file transfers, see [MIDI File Transfers](./midi_file_transfer.md).

Each song element can store multiple MIDI files and play back those files to control the local show element, allowing for pre-programmed shows to be played
with minimal network usage.

- For details regarding files, see [MIDI Files](./midi_file.md).
- For details regarding playback timing, see [MIDI Timing](./midi_timing.md).
