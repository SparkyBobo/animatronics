# LUT (Lookup Table) Configuration

## Overview

Lookup Tables (LUTs) define motion curves and behaviors for show elements. Each LUT describes how a motor or output should move over time to create smooth, choreographed actions timed to musical beats.

LUTs are stored as JSON files and loaded by show element boards. Each show element has a configuration file that specifies which LUTs to use and how to apply them.

## JSON LUT Format

### LUT File Structure

A single LUT file defines one motion curve with metadata:

```json
{
  "name": "drum_strike_fast",
  "element": "drums",
  "motor": "arm_strike",
  "description": "Fast drum strike motion for downbeat",
  
  "duration_ms": 500,
  "beat_duration": 12,
  "tempo_bpm": 120,
  
  "reset_value": 0,
  
  "velocity_mode": "lut_scaling",
  "velocity_range": [1, 127],
  
  "curve": [0, 5, 15, 28, 42, 55, 65, 72, 77, 80, 82, 83, 84, 85, 85, 84, 82, 80, 77, 72, 65, 55, 42, 28, 15, 5, 0]
}
```

### Field Descriptions

#### Metadata
- **name** (string, required): Unique identifier for this LUT, used in MIDI file event mappings
- **element** (string, required): Show element this LUT belongs to (e.g., "joey", "drums", "lights", "groove_bass")
- **motor** (string, required): Specific motor or output this LUT controls (e.g., "arm_strike", "mouth", "head_rotation")
- **description** (string, optional): Human-readable description of the motion

#### Timing
- **duration_ms** (integer, required): Total motion duration in milliseconds
- **beat_duration** (integer, optional): Duration in beats at standard tempo (for reference)
- **tempo_bpm** (integer, optional): Reference tempo used to calculate beat_duration (typically 120 BPM)

#### Motor Behavior
- **reset_value** (number, required): Default position/state when motion is not active
  - Typically 0 (off, closed, home position)
  - Range depends on motor hardware (0-255 for 8-bit PWM, 0-1.0 for normalized)
  - Must be within valid range for this motor
  
- **velocity_mode** (string, required): How velocity affects motion execution
  - **"lut_scaling"**: Velocity scales the number of LUT points used
    - Velocity 127 = use all points
    - Velocity 64 = use ~50% of points (compress timing)
    - Velocity 1 = use 1st point only (nearly instant)
  - **"direct_position"**: Velocity directly sets target position
    - Example: For mouth motor, velocity 0=closed, velocity 127=fully open
    - LUT is ignored; motion goes directly to velocity position
    - Only `curve[0]` and `curve[-1]` are relevant (start and end)
  - **"intensity"**: Velocity scales curve amplitude
    - Example: LUT represents 0-100% motion; velocity 64 = 50% amplitude
    - Useful for variable-intensity strikes or movements

- **velocity_range** (array, optional): Valid velocity range [min, max]
  - Default: [1, 127]
  - Velocities outside this range are clamped to min/max

#### Curve Data
- **curve** (array of numbers, required): Position values at each time step
  - Length determines resolution (number of points)
  - Values: 0-255 (8-bit) or 0-1.0 (normalized), depending on motor
  - First value = starting position (typically matches reset_value)
  - Last value = ending position
  - One value per Timing Clock (or every N clocks—see resolution)

## Curve Examples

### Example 1: Drum Strike (Fast)
Fast down-and-up motion for hitting a drum on the beat:

```json
{
  "name": "drum_strike_fast",
  "element": "drums",
  "motor": "arm_strike",
  "description": "Fast strike—arm accelerates down, hits on beat, rebounds up",
  "duration_ms": 500,
  "beat_duration": 12,
  "reset_value": 0,
  "velocity_mode": "lut_scaling",
  "curve": [0, 5, 15, 28, 42, 55, 65, 72, 77, 80, 82, 83, 84, 85, 85, 84, 82, 80, 77, 72, 65, 55, 42, 28, 15, 5, 0]
}
```

**Explanation:**
- 24 points = 500ms / ~21ms per clock = 1 point per Timing Clock at 120 BPM
- Motion accelerates from 0 to peak (85) at point ~12 (middle of 500ms)
- Peak represents the strike hitting the drum head
- Then decelerates back to 0 (reset position)
- With velocity scaling: High velocity = full 24 points; low velocity = fewer points (faster motion)

### Example 2: Mouth Movement (Velocity = Direct Position)

```json
{
  "name": "mouth_open",
  "element": "joey",
  "motor": "mouth",
  "description": "Mouth open amount controlled by velocity (0=closed, 127=wide open)",
  "duration_ms": 100,
  "reset_value": 0,
  "velocity_mode": "direct_position",
  "curve": [0, 127]
}
```

**Explanation:**
- Velocity directly sets mouth opening
- Velocity 0 = position 0 (closed)
- Velocity 127 = position 127 (fully open)
- Intermediate velocities interpolate between 0 and 127
- `duration_ms` is instantaneous (or as fast as motor allows)
- No lookahead needed—mouth moves immediately with velocity change

### Example 3: Head Rotation (Intensity Scaling)

```json
{
  "name": "head_wobble",
  "element": "joey",
  "motor": "head_rotation",
  "description": "Wobble left-right; velocity controls wobble intensity",
  "duration_ms": 800,
  "reset_value": 127,
  "velocity_mode": "intensity",
  "curve": [127, 110, 90, 110, 130, 110, 90, 110, 130, 110, 90, 110, 127]
}
```

**Explanation:**
- Base curve oscillates around center (127): left (90), center (127), right (130)
- `reset_value` is center (127)
- Velocity 127 = full amplitude wobble
- Velocity 64 = ~50% amplitude wobble (deviation from center is halved)
- Velocity 1 = almost no wobble (stays near center)

## Element Configuration Files

Each show element has a master configuration file that lists all available LUTs and element-specific settings:

```json
{
  "element_name": "joey",
  "element_type": "singer",
  "midi_channel": 1,
  "description": "Joey, male lead singer with head, mouth, arm movements",
  
  "motors": {
    "mouth": {
      "type": "servo",
      "range": [0, 180],
      "reset_value": 0,
      "description": "Mouth open/close (servo angle 0=closed, 180=wide open)"
    },
    "head_rotation": {
      "type": "servo",
      "range": [0, 180],
      "reset_value": 90,
      "description": "Head left-right (servo angle 0=left, 90=center, 180=right)"
    },
    "arm_wave": {
      "type": "servo",
      "range": [0, 255],
      "reset_value": 128,
      "description": "Arm wave motion (0=down, 128=neutral, 255=up)"
    }
  },
  
  "luts": {
    "mouth_open": "luts/joey_mouth_open.json",
    "mouth_talking": "luts/joey_mouth_talking.json",
    "head_nod": "luts/joey_head_nod.json",
    "head_shake": "luts/joey_head_shake.json",
    "arm_wave_fast": "luts/joey_arm_wave_fast.json",
    "arm_wave_slow": "luts/joey_arm_wave_slow.json"
  },
  
  "note_mappings": {
    "60": {"lut": "mouth_open", "motor": "mouth", "velocity_mode": "direct_position"},
    "61": {"lut": "mouth_talking", "motor": "mouth", "velocity_mode": "lut_scaling"},
    "64": {"lut": "head_nod", "motor": "head_rotation", "velocity_mode": "lut_scaling"},
    "65": {"lut": "head_shake", "motor": "head_rotation", "velocity_mode": "lut_scaling"},
    "72": {"lut": "arm_wave_fast", "motor": "arm_wave", "velocity_mode": "lut_scaling"},
    "73": {"lut": "arm_wave_slow", "motor": "arm_wave", "velocity_mode": "lut_scaling"}
  }
}
```

### Element Configuration Fields

- **element_name** (string): Unique identifier (used in MIDI file track metadata)
- **element_type** (string): Category (e.g., "singer", "drummer", "lights", "effects")
- **midi_channel** (integer): MIDI channel this element listens on (1-15)
- **description** (string): Human-readable description

- **motors**: Map of motor names to hardware specifications
  - **type**: "servo", "pwm_motor", "led", "relay", etc.
  - **range**: Valid output values [min, max]
  - **reset_value**: Default position when inactive
  - **description**: What this motor does

- **luts**: Map of LUT names to file paths
  - Key = LUT name (used in note mappings)
  - Value = relative path to LUT JSON file

- **note_mappings**: Map of MIDI notes to LUT actions
  - Key = MIDI note number (as string)
  - Value = object specifying which LUT to use and how

## Creating LUTs

### Step 1: Define Motion Characteristics

Before creating a LUT, know:
- **Duration:** How long should the motion take? (100ms-2000ms typical)
- **Start position:** Where does motion begin? (typically reset_value)
- **Peak/target:** What's the furthest point reached?
- **End position:** Where does motion finish? (typically reset_value)
- **Shape:** Is motion smooth? Accelerating? Decelerating? Bouncy?

### Step 2: Determine Resolution

- **Number of points** = Duration / Clock Interval
- At 120 BPM: Clock Interval ≈ 20.8ms
- 500ms motion ÷ 20.8ms/clock ≈ 24 points
- More points = smoother curve but more data
- Fewer points = jerkier motion but less data

### Step 3: Define Curve Points

Generate curve using:

**Option A: Mathematical Function**
Use sinusoidal or polynomial curve:
```
For drum strike (acceleration down, fast rebound up):
- First 50%: acceleration curve (0 → peak)
- Second 50%: deceleration curve (peak → 0)
- Use sine wave or cubic ease-in/ease-out
```

**Option B: Measured Motion**
- Record actual motor movement
- Sample position at regular intervals
- Normalize to 0-255 or 0-1.0 range

**Option C: Animation/Timeline**
- Create animation in graphics software
- Export position keyframes
- Sample at required resolution

### Step 4: Validate

- Ensure first and last points match reset_value
- Check that peak values are within motor range
- Verify curve is physically achievable by motor
- Test in Real-Time Mode before using in files

## Velocity Mode Selection

Choose velocity mode based on motor type and desired effect:

| Motor Type | Typical Velocity Mode | Rationale |
|------------|----------------------|-----------|
| Mouth (singer) | direct_position | Velocity = mouth opening (0-127) |
| Drum arm | lut_scaling | Velocity = strike intensity (full vs. soft hit) |
| Head rotation | lut_scaling | Velocity = wobble intensity |
| LED brightness | direct_position | Velocity = brightness (0-127) |
| Eye color | lut_scaling | Velocity = color intensity or cycle speed |
| Arm wave | intensity | Velocity = wave size (small to large) |

## File Organization

Suggested directory structure:

```
element_configs/
├── joey.json
├── lizzie.json
├── drums.json
├── lights.json
└── luts/
    ├── joey_mouth_open.json
    ├── joey_mouth_talking.json
    ├── joey_head_nod.json
    ├── joey_head_shake.json
    ├── joey_arm_wave_fast.json
    ├── joey_arm_wave_slow.json
    ├── drums_strike_fast.json
    ├── drums_strike_slow.json
    ├── lights_pulse.json
    └── ... (more LUTs)
```

## Testing LUTs

### In Real-Time Mode
1. Send Note On for the desired LUT with various velocities
2. Observe motor behavior and smoothness
3. Adjust curve points if motion is jerky or wrong speed
4. Verify reset_value is correct

### In File Playback Mode
1. Create short MIDI file with events using the LUT
2. Transfer file to show element
3. Initiate playback
4. Verify:
   - Motion starts at correct calculated time (accounting for duration)
   - Motion reaches target position on beat
   - Reset value is held between motions
   - No jerkiness or skipping

## Troubleshooting

**Motion is jerky or has gaps:**
- Increase number of curve points (higher resolution)
- Check curve for sudden jumps between adjacent points
- Ensure Timing Clock is accurate and consistent

**Motion doesn't hit the beat:**
- Verify duration_ms is accurate (test motor timing independently)
- Check that lookahead window is large enough
- Verify MIDI event is at correct beat position in file

**Motion skips startup or overshoots:**
- Ensure first point matches reset_value
- Verify curve doesn't exceed motor's valid range
- Check for velocity mode misapplication

**Reset value not applied:**
- Verify reset_value is defined in LUT
- Check that motor can actually reach reset_value (within hardware range)
- Ensure Note Off or motion end is being processed correctly
