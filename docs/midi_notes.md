# MIDI Notes, Controls, and Programs

## Overview

This document defines note, control change, and program change mappings for each show element. Mappings are organized by element type and coordinate with [LUT Configuration](./midi_lut_configuration.md) for motion execution.

For details on MIDI message encoding, see table at end of document.

## Show Elements and Channels

See [MIDI Channels](./midi_channel.md) for full channel assignments. Common elements:
- **Channel 1:** Joey (male singer)
- **Channel 2:** Lizzie (female singer)
- **Channel 3:** Chorus singers
- **Channel 4:** Drums/Percussion
- **Channel 5:** Groove (bass guitar)
- **Channel 6:** Slash (electric guitar)
- **Channel 7:** Tickles (piano/keyboard)
- **Channel 13:** Lights
- **Channel 14:** Special Effects
- **Channel 15:** Video playback

---

## Rhythmic Elements: Foot, Hand, Hip Taps

Show elements supporting rhythmic operations (Joey, Lizzie, Chorus, Slash, Groove, Tickles) respond to C1-B1 octave notes for synchronized rhythmic movements.

### Note Mappings - Rhythm (C1-B1, Notes 12-23)

| Note | MIDI # | Name | Action | Velocity | LUT Mode | Description |
|------|--------|------|--------|----------|----------|-------------|
| C1 | 12 | Beat Reference | Sync pulse (no direct action) | N/A | N/A | Used to establish beat; others sync to this |
| D1 | 14 | Foot Tap | Tap foot to beat | 0-127 | lut_scaling | Foot taps in rhythm; velocity = intensity |
| E1 | 16 | Finger/Hand Tap | Tap finger/hand to beat | 0-127 | lut_scaling | Hand/finger taps in rhythm; Joey only |
| G#1 | 20 | Hip Rotate | Rotate hips to beat | 0-127 | intensity | Hip rotation side-to-side; Joey/Lizzie only |

---

## Head Rotation

Show elements with rotating heads (Joey, Lizzie, Chorus) respond to C1-B1 octave notes for head movement.

### Note Mappings - Head Rotation (F1-G1, Notes 17-19)

| Note | MIDI # | Name | Action | Velocity | LUT Mode | Description |
|------|--------|------|--------|----------|----------|-------------|
| F1 | 17 | Head Left | Rotate head left | 0-127 | direct_position | Rotate head left; velocity = rotation amount |
| F#1 | 18 | Head Beat | Rotate to beat | 0-127 | lut_scaling | Rhythmic head bobbing; velocity = intensity |
| G1 | 19 | Head Right | Rotate head right | 0-127 | direct_position | Rotate head right; velocity = rotation amount |

---

## Arm/Hand Movement (Lizzie)

Lizzie supports arm rotation and gestures.

### Note Mappings - Arm Rotation (TBD)

| Note | MIDI # | Name | Action | Velocity | LUT Mode | Description |
|------|--------|------|--------|----------|----------|-------------|
| TBD | | Left Arm Rotate | Rotate left arm | 0-127 | direct_position | Left arm rotation (angle based on velocity) |
| TBD | | Left Arm Beat | Rotate left arm to beat | 0-127 | lut_scaling | Left arm rhythmic motion |
| TBD | | Right Arm Rotate | Rotate right arm | 0-127 | direct_position | Right arm rotation (angle based on velocity) |

---

## Vocals and Mouth Movement

Vocal show elements (Joey, Lizzie, Chorus, Tickles, Keyboards) respond to C4-B4 octave notes for mouth control. Velocity controls mouth opening amount.

### Note Mappings - Vocals (C4-B4, Notes 60-71)

| Note | MIDI # | Name | Action | Velocity | LUT Mode | Description |
|------|--------|------|--------|----------|----------|-------------|
| C4 | 60 | Mouth A | Mouth open | 0-127 | direct_position | Mouth shape A; velocity = openness (0=closed, 127=wide) |
| C#4 | 61 | Mouth E | Mouth open | 0-127 | direct_position | Mouth shape E; vowel-like positions |
| D4 | 62 | Mouth I | Mouth open | 0-127 | direct_position | Mouth shape I |
| D#4 | 63 | Mouth O | Mouth open | 0-127 | direct_position | Mouth shape O |
| E4 | 64 | Mouth U | Mouth open | 0-127 | direct_position | Mouth shape U |
| F4 | 65 | Mouth Consonant | Mouth position | 0-127 | direct_position | Mouth consonant position |
| F#4 | 66 | Reserved | | | | |
| G4 | 67 | Reserved | | | | |
| G#4 | 68 | Reserved | | | | |
| A4 | 69 | Reserved | | | | |
| A#4 | 70 | Reserved | | | | |
| B4 | 71 | Reserved | | | | |

**Note:** Mouth velocity interpretation: 0 = closed, 127 = fully open. Intermediate values map to mouth opening percentage. Last note takes precedence if multiple notes active.

---

## Guitar and Bass: Fret Hand Position

Guitar (Slash) and bass (Groove) show elements with fret hand movement respond to notes in C0-B5 range to position left hand on fretboard.

### Note Mappings - Fret Hand Position (C0-B5, Notes 12-83)

| Note | MIDI # | Name | Position | Description |
|------|--------|------|----------|-------------|
| B1 | 35 | Fret Position 1 | Left-most position | Left hand at left-most fret position |
| ... | 36-70 | Fret Positions 2-35 | Intermediate | Positions across fretboard (16-fret mapping) |
| C5 | 72 | Fret Position 37 | Right-most position | Left hand at right-most fret position |
| B5 | 83 | Fret Position 48 | Alternate range | Extended range for multi-octave reach |

**Note:** Fret positions use velocity as intensity of finger pressure (affects tone/dynamics). Pitch bend used for string bending and rotation (see below).

---

## Guitar and Bass: Pitch Bend and Rotation

Pitch wheel change messages control guitar rotation and string bending.

### Pitch Wheel Mappings - Guitar/Bass Rotation

| Pitch Bend | Effect | Description |
|------------|--------|-------------|
| 0 (down) | Rotate CCW | Guitar rotates counter-clockwise |
| 8192 (center) | No rotation | Guitar centered |
| 16383 (up) | Rotate CW | Guitar rotates clockwise |

**Effect:** When active note(s) on fretboard, pitch bend rotates guitar body. Regardless of whether fret note is active, rotation can be applied. Controls visual rotation of instrument body.

---

## Eye Color

Show elements with eyes (Joey, Lizzie, Groove's bass, Tickles' keyboard) support eye color control.

### Note Mappings - Eye Color (C7-B8, Notes 108-119)

| Note Range | Name | Description |
|------------|------|-------------|
| Notes 108-113 (C7-F#7) | Primary Colors | TBD - to be defined per element |
| Notes 114-119 (G7-B7) | Secondary Colors | TBD - to be defined per element |

---

## Control Changes (CC)

General control changes available across show elements (element-specific mappings TBD):

| CC # | Name | Purpose | Value Range | Notes |
|------|------|---------|-------------|-------|
| TBD | | | | To be defined per element |

---

## Program Changes

Program changes for selecting motion profiles or presets (element-specific mappings TBD):

| Program # | Profile | Description |
|-----------|---------|-------------|
| TBD | | To be defined per element |

---

## MIDI Message Encoding Reference

| Message | Status | Data Byte(s) | Description |
|---------|--------|--------------|-------------|
| Note Off | 1000nnnn | 0kkkkkkk 0vvvvvvv | Note release; k=key, v=velocity |
| Note On | 1001nnnn | 0kkkkkkk 0vvvvvvv | Note press; k=key, v=velocity |
| Control Change | 1011nnnn | 0ccccccc 0vvvvvvv | Controller change; c=controller, v=value |
| Program Change | 1100nnnn | 0ppppppp | Program select; p=program number |
| Pitch Wheel | 1110nnnn | 0lllllll 0mmmmmmm | 14-bit pitch; l=LSB, m=MSB |

---

## Notes for Future Documentation

- Complete eye color mappings as each element is configured
- Define element-specific control changes and program changes
- Test all note mappings in Real-Time Mode before deploying in MIDI files
- Refer to [LUT Configuration](./midi_lut_configuration.md) for motion curve definitions and velocity semantics
- Document any special behaviors or conflicts between simultaneous notes

