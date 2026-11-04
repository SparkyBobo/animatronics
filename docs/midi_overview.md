# MIDI

## Overview

The DaBones use MIDI to synchronize and play song elements. MIDI was chosen because:

1. MIDI seemed like a natural fit for controlling things that are based on music
2. MIDI is cheap to implement from a software and hardware perspective
3. MIDI works well over relatively short links, and the song elements are closely grouped together
4. MIDI has a robust protocol definition capable of handling all aspects of the required communication
5. MIDI interoperates with Digital Audio Workstations (DAWs) well so the DAW can become the programming surface

## Operational Modes

The DaBones system operates in two distinct modes:

**File Playback Mode (Production):** Each song element stores locally cached MIDI files. The master controller broadcasts Song Select to load a file, then broadcasts Timing Clock and Song Position Pointer. Each show element independently executes its track using predictive motion planning—scanning ahead to queue motions that will land precisely on musical beats. This enables smooth, natural choreography during shows.

**Real-Time Mode (Design/Testing):** Show elements respond to individual MIDI note, control change, and program change messages sent to their assigned MIDI channel. Execution is immediate, with no lookahead or predictive motion. This mode is used for interactive testing, troubleshooting, and choreography design iteration.

For a detailed explanation of modes and the design workflow, see [System Architecture](./midi_architecture.md).

## System Organization

The DaBones use MIDI channels to target individual song elements, with one MIDI channel for each "instrument", i.e., character or song element, e.g., lights.
This allows each song element to be targeted individually or as a single group. For a list of MIDI channels, see [MIDI Channels](./midi_channel.md).

The master controller uses MIDI channel 0 for playback synchronization (Song Select, Timing Clock, Song Position Pointer, and file transfers). Individual show elements listen on dedicated channels for real-time control messages.

## Documentation Organization

- **System Architecture:** For overview, hardware layout, and operational workflow, see [System Architecture](./midi_architecture.md)
- **Message Reference:** For MIDI message types and encoding, see [MIDI Messages](./midi_messages.md)
- **File Format:** For MIDI file structure and metadata, see [MIDI Files](./midi_file.md)
- **Event Mapping:** For note, control, and program mappings, see [MIDI Notes, Controls, and Programs](./midi_notes.md)
- **Playback Control:** For playback-related messages and motion planning, see [MIDI Playback](./midi_playback.md)
- **File Transfer:** For file transfer protocol and procedures, see [MIDI File Transfers](./midi_file_transfer.md)
- **Timing:** For timing calculations and synchronization, see [MIDI Timing](./midi_timing.md)
