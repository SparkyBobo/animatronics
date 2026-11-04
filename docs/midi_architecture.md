# System Architecture

## Overview

The DaBones system is a distributed, synchronized animatronic control platform built on Raspberry Pi Pico RP2040 boards running CircuitPython. The system synchronizes multiple show elements to perform choreographed motions precisely timed to music using MIDI as the coordination protocol.

The architecture enables two distinct operational modes:
1. **File Playback Mode** - Production show playback with predictive motion execution
2. **Real-Time Mode** - Interactive control for testing and design iteration

## Hardware Architecture

### Master Controller Board
- **Hardware:** Raspberry Pi Pico RP2040 with MIDI interface
- **Role:** Central synchronization authority
- **Connections:** Connected to DAW (Digital Audio Workstation) via MIDI, broadcasts to all show elements

### Show Element Boards
- **Hardware:** Raspberry Pi Pico RP2040 with MIDI input, motor drivers, sensors, lights, or other actuators
- **Role:** Autonomous motion executors
- **Connections:** MIDI input from master controller, local hardware outputs

### MIDI Network
- Master broadcasts on MIDI channel 0 (system messages)
- Each show element listens on a dedicated channel for real-time control messages
- System Exclusive messages used for file transfers

## Operational Modes

### Mode 1: File Playback Mode (Production)

**Purpose:** Execute choreographed shows with precise motion timing

**Workflow:**
1. Choreographer creates MIDI file offline in DAW with all events and timing
2. File is transferred to show element via System Exclusive message
3. Master broadcasts Song Select to load the file on all show elements
4. Master broadcasts Song Position Pointer (optional, for seeking)
5. Master broadcasts Timing Clock (24 clocks per quarter note)
6. Each show element independently executes its track using predictive motion planning

**Show Element Behavior:**
- Load MIDI file matching Song Select message
- Scan ahead in file to identify upcoming events (lookahead window, e.g., 500ms)
- For each upcoming event, calculate start time: `Start Time = Event Time - Motion Duration`
- At calculated start time, begin executing motion from lookup table (LUT)
- Follow LUT curve from start through event time, reaching target position exactly on beat
- Continue scanning and executing throughout playback

**Advantages:**
- Smooth, natural motion with predictable timing
- Multiple show elements run in parallel without network overhead
- Animatronics can anticipate musical events and choreograph accordingly
- Robust—clock dropouts don't cause synchronization loss (local playback continues)

### Mode 2: Real-Time Mode (Design/Testing)

**Purpose:** Interactive testing and design of show elements

**Workflow:**
1. Designer sends Note On/Off, Control Change, or Program Change messages
2. Show element receives message on its MIDI channel
3. Show element executes command immediately
4. Designer observes response and iterates

**Show Element Behavior:**
- Listen for incoming MIDI messages on assigned channel
- Execute message immediately (no lookahead, no motion prediction)
- Ignore Timing Clock and Song Position Pointer
- Return to idle/rest position between messages

**Advantages:**
- Immediate feedback for design and troubleshooting
- Simple, deterministic behavior
- Can diagnose hardware and connectivity issues

**Disadvantages:**
- No predictive motion (may appear jerky or delayed)
- Not suitable for final performance (lacks natural motion)

## Design Workflow

### Iterative Choreography Development

```
1. Program Phase (Offline)
   └─ Edit MIDI file in DAW
   └─ Arrange events and timing
   └─ Save file

2. Transfer Phase
   └─ Transfer MIDI file to show element boards
   └─ Verify transfer success

3. Playback Phase
   └─ Initiate playback with Timing Clock
   └─ Observe motion timing and choreography
   └─ Take notes on issues

4. Adjust Phase
   └─ If timing is off: Tweak event timing in DAW file
   └─ If motion is wrong: Adjust LUT or event mapping
   └─ If isolated: Use Real-Time mode to test individual element
   └─ Return to step 2

5. Verify Phase
   └─ Run complete playback multiple times
   └─ Verify all elements hit their marks on beat
   └─ Lock file as final show version
```

This mirrors the traditional lighting design workflow: program offline, test playback, iterate, finalize.

## Master Controller Software Requirements

### Messaging
- **Song Select:** Broadcast to all show elements to load a specific MIDI file
- **Song Position Pointer:** Optional seek/pause messages to move playback position
- **Timing Clock:** Generate 24 clocks per quarter note at precise intervals
- **Start/Continue/Stop:** Playback control messages
- **Active Sensing:** Send every 300ms maximum to maintain connection

### File Transfer
- Implement System Exclusive file transfer protocol
- Calculate file transfer checksums
- Handle retransmit if needed
- Verify successful transfer to all elements

### DAW Integration
- Receive MIDI messages from DAW
- Convert DAW tempo to Timing Clock generation rate
- Passthrough real-time control messages to show elements (for Real-Time mode)
- Display connection status and sync status

### State Management
- Track which song/file is currently selected
- Track current playback position
- Monitor all show elements for connection status

## Show Element Software Requirements

### File Storage and Management
- Store multiple MIDI files locally on RP2040 (flash or SD card)
- Organize files by song number for quick lookup
- Implement System Exclusive file transfer receiver
- Validate file checksums and integrity
- Report transfer success/failure via LED or other indicator

### File Playback Mode
1. **Initialization:**
   - Listen for Song Select message on MIDI channel 0
   - Search local file storage for matching file
   - Load file into memory/buffer

2. **Playback Control:**
   - Listen for Timing Clock on channel 0
   - Listen for Song Position Pointer (seek/pause)
   - Listen for Start/Continue/Stop commands
   - Reset playback position on Start
   - Pause on Stop (maintain position)

3. **Motion Planning (Lookahead):**
   - Maintain a lookahead window (suggested: 500ms or 24 beats)
   - Scan upcoming MIDI events on element's assigned channel within lookahead window
   - For each upcoming event:
     - Look up motion type from MIDI note number
     - Retrieve LUT configuration for that motion (includes duration and reset value)
     - Calculate: `Start Time = Event Time - Motion Duration`
     - Plan motion to start at calculated time

4. **Motion Execution:**
   - On each Timing Clock, check if a new motion should start
   - If motion should start now:
     - Retrieve LUT curve from configuration
     - Apply velocity modifier if applicable (direct position or LUT scaling)
     - Begin stepping through curve points
   - For each subsequent clock:
     - If motion in progress, advance to next LUT point
     - Apply motor command (PWM, direction, etc.)
   - When motion ends:
     - Return motor to its **reset value** (defined in LUT configuration)
     - Hold reset value until next motion starts

5. **Playback Continuation:**
   - Continue scanning, planning, and executing throughout playback
   - Each motor operates independently with no queueing

### Real-Time Mode
1. Listen for incoming MIDI messages on assigned channel
2. Parse message type (Note On/Off, Control Change, Program Change)
3. Map to local hardware action using note/control mappings (see [MIDI Notes, Controls, and Programs](./midi_notes.md))
4. For Note On: Apply velocity directly or use velocity to select action intensity
5. For Note Off or when no messages received: Return motor/output to **reset value** (defined in LUT configuration or element config)

Reset values examples:
- **Mouth motor:** Fully closed (value 0)
- **Drum arm:** Home position (value 0 or configured position)
- **LED:** Off (value 0)
- **Head rotation:** Center (value 127 or configured center)

### Timing Requirements
- Timing Clock interval precision: ±5% tolerance (derived from 300ms Active Sensing window)
- Motion LUT execution: Follow curve points at each clock interval
- Lookahead window: Sufficient to accommodate longest motion type

### Motion Planning and Execution
**Lookahead:**
- Scan file for upcoming events (next event per motor/control channel)
- For each event, look up motion duration in LUT configuration
- Calculate: `Start Time = Event Time - Motion Duration`
- Queue motion to start at calculated time

**Motion Execution Per Motor:**
- Each motor executes one motion at a time
- When new motion is queued and a motion is already in progress:
  - New motion calculation replaces existing motion plan
  - Current motion completes, then new motion begins at its calculated start time
- Follow LUT curve points sequentially, advancing one point per Timing Clock (or N clocks depending on LUT resolution)
- When motion ends, return motor to **reset/idle value** until next motion

**Multiple Motors:**
- Each motor operates independently
- Many motors can move simultaneously
- No queueing of multiple motions per motor

**Song Position Pointer (Seek):**
- When Position Pointer received mid-playback:
  - Return all motors to their reset/idle values
  - Recalculate next upcoming events from new file position
  - Restart lookahead from there

### Lookup Table (LUT) Configuration
For detailed LUT format, schema, and configuration examples, see [LUT Configuration](./midi_lut_configuration.md).

**Overview:**
- **Format:** JSON files defining motion curves per motor/element
- **Content:** Array of position values representing motor state at each time step
- **Resolution:** Number of points in LUT determines granularity (typically 24-96 points)
- **Timing:** Each point corresponds to one or more Timing Clocks
- **Reset Value:** Defined per motor—idle position when no motion in progress
- **Velocity Interpretation:** Depends on motor type:
  - **Direct Position Control:** Velocity maps directly to final position (e.g., mouth opening)
  - **LUT Scaling:** Velocity scales how many LUT points to use (e.g., 127=full, 63=half)

Example structure:
```json
{
  "motor_name": "drum_arm",
  "duration_ms": 500,
  "points_per_clock": 1,
  "reset_value": 0,
  "velocity_mode": "lut_scaling",
  "curve": [0, 5, 15, 28, 42, 55, 65, 72, 77, 80, 82, 83, 84, 85, 85, 84, 82, 80, 77, 72, 65, 55, 42, 28, 15, 5, 0]
}
```

For detailed format and per-element examples, see [LUT Configuration](./midi_lut_configuration.md).

## File Format Enhancements

### MIDI File Structure
- Standard MIDI Format 1 with multiple tracks
- Track 0: Metadata (tempo, time signature, sequence info)
- Tracks 1-N: Show element tracks with events

### Event Metadata
Events should include sufficient information for motion planning:
- **Standard MIDI Note On/Off:** Encodes motion type and target via note number
- **Control Changes:** May encode additional parameters (intensity, direction, speed override)
- **Program Changes:** Select motion profile or preset sequence

See [MIDI Notes, Controls, and Programs](./midi_notes.md) for detailed event mappings.

### LUT Selection
Motion type and LUT selection via:
- **Primary:** MIDI note number (defines which motion executes)
- **Modifiers:** Velocity (intensity), Control Changes (parameters)
- **Program Change:** Select alternate motion profiles if multiple available

## System Synchronization

### Clock Generation and Distribution
- Master generates Timing Clock at precise intervals: `Interval (ms) = (60,000 / Tempo BPM) / 24`
- Example: 120 BPM → 500ms per quarter note → ~20.8ms per clock
- All show elements synchronize motion execution to these clocks

### Position Synchronization
- Song Position Pointer (14-bit value) represents beats since start of song
- 1 beat = 6 Timing Clocks
- Master can send Position Pointer to seek or correct drift
- Show elements receiving Position Pointer:
  - Return all motors to their **reset values** (defined in LUT configuration)
  - Recalculate file position and next upcoming events from new location
  - Resume lookahead and playback from new position

### Connection Management
- Active Sensing message every 300ms maximum
- Loss of Active Sensing for >300ms indicates connection failure
- Show elements should stop, return to idle, and wait for reconnection
- Master should monitor loss of Active Sensing from show elements

## Design Considerations

### Motion Duration Metadata
Before designing a show, choreographer must know motion durations for each element:
- Drum strike: ~500ms
- Head rotation: ~400ms
- Arm wave: ~800ms
- Eye blink: ~200ms

These durations should be documented and available during file editing in DAW.

### Reset/Idle Values
Every motor and output element must have a defined **reset value**—the position or state when no motion is in progress.

Examples:
- **Mouth motor:** Fully closed (0)
- **Drum arm:** Home/strike position (defined per drum)
- **Head rotation:** Center position (127 or 50%)
- **LED intensity:** Off (0)
- **Eye color:** Off or default color (0)

Reset values are specified in LUT configuration files and applied:
- Between motions during file playback
- When Note Off received in Real-Time mode
- When Song Position Pointer (seek) received
- When connection is lost

### Lookahead Window Size
Larger lookahead allows earlier motion startup but uses more memory:
- Suggested minimum: 400ms (accommodates most motions)
- Suggested maximum: 2000ms (diminishing returns)
- Configure per show element based on available SRAM

### Timing Precision vs. Visual Quality
- Timing precision: ±1 Timing Clock (~20ms at 120 BPM)
- Visual quality: Depends on LUT curve smoothness and motor control resolution
- Higher clock accuracy requires lower jitter in RP2040 timer interrupt

## Failure Modes and Recovery

### Network Dropout
- Show element detects loss of Timing Clock
- Continues playback using cached tick rate until recovery
- May drift slightly, but motions continue
- Master can send Song Position Pointer to resync

### File Not Found
- Show element receives Song Select for missing file
- LED indicator shows error state
- Returns to idle, waits for valid Song Select

### Checksum Failure During Transfer
- File transfer aborts
- Previously stored file remains (if any)
- Show element ready for retry

## Testing and Validation

### Unit Testing (Real-Time Mode)
- Send individual Note On messages to test motor response
- Verify LED brightness control
- Test servo range limits
- Check sensor integration

### Integration Testing (Playback Mode)
- Load short test file (8-16 beats)
- Verify all elements execute at correct times
- Check motion curve smoothness
- Measure timing accuracy with oscilloscope or high-speed camera

### Full Show Validation
- Run complete show multiple times
- Verify no element drift or desynchronization
- Check for any motion collisions or interference
- Validate audio/visual synchronization
