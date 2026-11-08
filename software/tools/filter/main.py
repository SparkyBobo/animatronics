"""
Animacy

MIDI Filter utility

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
import gc
import mido

def keep_message(msg) -> int:
    if msg.type == "note_on":
        if (msg.channel >= 0 and msg.channel <= 6):
            return msg.channel
    if msg.type == "note_off":
        if (msg.channel >= 0 and msg.channel <= 6):
            return msg.channel
    return -1

mid = mido.MidiFile("..\\..\\2.mid")
output = [
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
    mido.MidiFile(ticks_per_beat=mid.ticks_per_beat),
]

for track in mid.tracks:
    new_tracks = [
        mido.MidiTrack(),
        mido.MidiTrack(),
        mido.MidiTrack(),
        mido.MidiTrack(),
        mido.MidiTrack(),
        mido.MidiTrack(),
        mido.MidiTrack(),
    ]

    output[0].tracks.append(new_tracks[0])
    output[1].tracks.append(new_tracks[1])
    output[2].tracks.append(new_tracks[2])
    output[3].tracks.append(new_tracks[3])
    output[4].tracks.append(new_tracks[4])
    output[5].tracks.append(new_tracks[5])
    output[6].tracks.append(new_tracks[6])

    absolute_tick = 0
    last_kept_tick = 0

    for msg in track:
        absolute_tick += msg.time

        ch = keep_message(msg)
        if (ch >= 0):
            new_tracks[ch].append(
                msg.copy(time=absolute_tick - last_kept_tick)
            )
            last_kept_tick = absolute_tick

output[0].save("2-1.mid")
output[1].save("2-2.mid")
output[2].save("2-3.mid")
output[3].save("2-4.mid")
output[4].save("2-5.mid")
output[5].save("2-6.mid")
output[6].save("2-7.mid")
