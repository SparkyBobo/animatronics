"""
Animacy

Performance control and event contracts.

Copyright (c) 2026 Sparky Bobo
"""

from __future__ import annotations

from animacy.contracts.color import Color
from animacy.contracts.curve import TimeCurve
from animacy.contracts.driver import DriverTransition

# Message id counter
_next_id = 0


# Generic performance events/transition.
class PerformanceEvent:
    def __init__(
        self,
        transition: DriverTransition = None,
        curve: TimeCurve = None,
        start: int = 0,
        end: int = 0,
    ):
        self.transition = transition
        self.curve = curve
        self.start = start
        self.end = end


# Generic performance message
class PerformanceMessage:
    def __init__(self, timecode: int = 0, events: list[PerformanceEvent] | None = None):
        # global _next_id
        # _next_id += 1
        # self._id: str = str(_next_id)
        self.timecode = timecode
        self.events = [] if events is None else events

    @property
    def id(self) -> str:
        return None
        # return f"{type(self).__name__ }({self._id})"


# Events that show
class PerformanceShowInformation(PerformanceMessage):
    def __init__(
        self, timecode: int = 0, song: str | None = None, name: str | None = None
    ):
        super().__init__(timecode)
        self.song = song
        self.name = name


# Events that define song and show intents.
class PerformanceControlMessage(PerformanceMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# Reset the performer to a baseline state, e.g., idle,
# and cleanup all show and song state, power up default.
class PerformanceSystemResetMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# File transfer header message, contains filename and action,
# such as verify, replace, delete.
class PerformanceFileHeaderMessage(PerformanceControlMessage):
    def __init__(
        self, timecode: int = 0, name: str | None = None, action: str | None = None
    ):
        super().__init__(timecode)
        self.name = name
        self.action = action


# File transfer content message, i.e., file bytes.
class PerformanceFileContentMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0, sequence: int = 0, data: bytes | None = None):
        super().__init__(timecode)
        self.sequence = sequence
        self.data = data


# File transfer end-of-file message, transfer complete.
class PerformanceFileCompleteMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0, checksum: int = 0):
        super().__init__(timecode)
        self.checksum = checksum


# Volume level message.
class PerformanceVolumeMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0, level: int = 0):
        super().__init__(timecode)
        self.level = level


# Load song (and prepare to play) message, e.g, read file
# and calculate.
class PerformanceLoadSongMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0, song: str | None = None):
        super().__init__(timecode)
        self.song = song


# Song start (from 0) message.
class PerformanceSongStartMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# Song continue (from current position) message.
class PerformanceSongContinueMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# Song stop (at current position) message.
class PerformanceSongStopMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# Song position message.
class PerformanceSongPositionMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0, position: int = 0):
        super().__init__(timecode)
        self.position = position


# Show clock message.
class PerformanceClockMessage(PerformanceControlMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# Events the define performer intent
class PerformanceDataMessage(PerformanceMessage):
    def __init__(
        self,
        timecode: int = 0,
        events: list[PerformanceEvent] | None = None,
    ):
        super().__init__(timecode, events)


# Resets the performer to a baseline position, ready to play a song.
class PerformanceResetEventMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0):
        super().__init__(timecode)


# Play a note in a note range. Used for actions that produce
# note ranges, like hand position on keyboard, neck position, tombone
# slide position, etc... (not singing)
class PerformancePlayNoteMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0, note: int = 0, intensity: int = 0):
        super().__init__(timecode)
        self.note = note
        self.intensity = intensity


# Play a note with a given technique. Used for actions that can produce
# different sounds givern the technique, like muted trumpet, strum, pick,
# pluck, slap, etc...
class PerformancePlayTechiqueMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0, technique: int = 0, intensity: int = 0):
        super().__init__(timecode)
        self.technique = technique
        self.intensity = intensity


# Bend a not in progress, like bending a string or vibrato
# including singing.
class PerformanceBendNoteMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0, bend: int = 0, intensity: int = 0):
        super().__init__(timecode)
        self.bend = bend
        self.intensity = intensity


# Play percussion which implies an quick attack and strike actions
# e.g., drumming, tambourine, percussion.
class PerformancePercussionStrikeMessage(PerformanceDataMessage):
    def __init__(
        self, timecode: int = 0, target: str | None = None, intensity: int = 0
    ):
        super().__init__(timecode)
        self.target = target
        self.intensity = intensity


# Intent to sing by opening the pie hole.
class PerformanceSingMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0, intensity: int = 0):
        super().__init__(timecode)
        self.intensity = intensity


# Turn the neck to a specific position, but not rythmic,
# i.e., a single one-time motion where position is important.
class PerformanceNeckPositionMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0, position: int = 0, intensity: int = 0):
        super().__init__(timecode)
        self.position = position
        self.intensity = intensity


# Move rythmically to the beat, i.e, periodic motion
# where timing is important, e.g. foot tap, hip swing, next twist
class PerformanceRythmicMotionMessage(PerformanceDataMessage):
    def __init__(self, timecode: int = 0, frequency: int = 0, intensity: int = 0):
        super().__init__(timecode)
        self.frequency = frequency
        self.intensity = intensity


# Move rythmically to the beat, i.e, periodic motion
# where timing is important, e.g. foot tap, hip swing, next twist
class PerformanceEyeMessage(PerformanceDataMessage):
    def __init__(
        self, timecode: int = 0, color: Color = None, intensity: int = 0, fade: int = 0
    ):
        super().__init__(timecode)
        self.color = color
        self.intensity = intensity
        self.fade = fade


# The result from a message processor
class PerformanceMessageResult:
    """Performance message processing result"""

    SKIPPED = 0  # No action taken
    QUEUED = 1  # Message was queued
    HANDLED = 101  # Action taken
    TERMINATE = 102  # Do not continue propogation


# A processing protocol for processing performance messages
class PerformanceMessageProcessor:
    def process(self, message: PerformanceMessage) -> PerformanceMessageResult: ...
