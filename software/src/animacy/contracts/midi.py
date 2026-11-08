"""
Animacy

Midi message contracts.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.performance import PerformanceMessage, PerformanceMessageProcessor

# Generic Midi message
class MidiMessage():
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, MidiMessage)
            and type(self) is type(other)
            and self.__dict__ == other.__dict__
        )

# Bad Midi message
class MidiIncompleteMessage(MidiMessage):
    pass

# Unknown Midi message
class MidiUnknownMessage(MidiMessage):
    pass

# Unknown Midi message
class MidiChannelMessage(MidiMessage):

    def __init__(self, channel: int = 0):
        super().__init__()
        self.channel = channel

# Midi Note Off
class MidiNoteOff(MidiChannelMessage):

    def __init__(self, channel: int = 0, note: int=0, velocity: int=0):
        super().__init__(channel)
        self.note = note
        self.velocity = velocity

# Midi Note On
class MidiNoteOn(MidiChannelMessage):

    def __init__(self, channel: int = 0, note: int=0, velocity: int=0):
        super().__init__(channel)
        self.note = note
        self.velocity = velocity

# Midi Control Change
class MidiControlChange(MidiChannelMessage):

    def __init__(self, channel: int = 0, control: int=0, value: int=0):
        super().__init__(channel)
        self.control = control
        self.value = value

# Midi Program Change
class MidiProgramChange(MidiChannelMessage):

    def __init__(self, channel: int = 0, program: int=0):
        super().__init__(channel)
        self.program = program

# Midi Pitch Bend
class MidiPitchBend(MidiChannelMessage):

    def __init__(self, channel: int = 0, bend: int=0):
        super().__init__(channel)
        self.bend = bend

# All Sound Off
class MidiDeviceMode(MidiControlChange):

    def __init__(self, channel: int = 0, control: int = 0, value: int = 0):
        super().__init__(channel=channel, control=control, value=value)

# All Sound Off
class MidiAllSoundOff(MidiChannelMessage):

    def __init__(self, channel: int = 0):
        super().__init__(channel=channel)

# All Notes Off
class MidiAllNotesOff(MidiChannelMessage):

    def __init__(self, channel: int = 0):
        super().__init__(channel=channel)

# Universal System Exclusive
class MidiUniversalSystem(MidiMessage):

    def __init__(self, channel: int=0):
        super().__init__()
        self.channel = channel

# File transfer header message
class MidiFileHeader(MidiUniversalSystem):

    def __init__(self, channel: int=0, length: int = 0, name: str = None):
        super().__init__(channel)
        self.length = length
        self.name = name


# File transfer content message, i.e., file bytes.
class MidiFileContent(MidiUniversalSystem):

    def __init__(self, channel: int=0, data: bytes = None):
        super().__init__(channel)
        self.data = data

# File transfer end-of-file message, transfer complete.
class MidiFileComplete(MidiUniversalSystem):

    def __init__(self, channel: int=0):
        super().__init__(channel)

# Open file (and prepare to play) message, e.g, read file
# and calculate.
class MidiFileOpen(MidiUniversalSystem):
    # song id.
    def __init__(self, channel: int=0, id: str = None):
        super().__init__(channel)
        self.id = id

# Cancel
class MidiCancel(MidiUniversalSystem):

    def __init__(self, channel: int=0):
        super().__init__(channel)

# NACK
class MidiNack(MidiUniversalSystem):

    def __init__(self, channel: int=0):
        super().__init__(channel)

# ACK
class MidiAck(MidiUniversalSystem):

    def __init__(self, channel: int=0):
        super().__init__(channel)

# Volume level message.
class MidiVolumeSet(MidiUniversalSystem):

    def __init__(self, channel: int=0, level: int = 0):
        super().__init__(channel)
        self.level = level

# Load song (and prepare to play) message, e.g, read file
# and calculate.
class MidiSongSelect(MidiMessage):

    def __init__(self, song: int = 0):
        super().__init__()
        self.song = song

# Song position message.
class MidiSongPosition(MidiMessage):

    def __init__(self, position: int = 0):
        super().__init__()
        self.position = position

# Tune request/
class MidiTuneRequest(MidiMessage):
    pass

# Real time
class MidiClock(MidiMessage):
    pass

# Song start (from 0) message.
class MidiSongStart(MidiMessage):
    pass

# Song continue (from current position) message.
class MidiSongContinue(MidiMessage):
    pass

# Song stop (at current position) message.
class MidiSongStop(MidiMessage):
    pass

# Active Sensing (keep-alive)
class MidiActiveSensing(MidiMessage):
    pass

# Reset
class MidiReset(MidiMessage):
    pass

# Track info
class MidiFileInfo:

    def __init__(self, sequence: str = None, name: str = None, tempo: int = -1, miditicks_per_quarter: int = -1):
        super().__init__()
        self.sequence = sequence
        self.name = name
        self.tempo = tempo
        self.miditicks_per_quarter = miditicks_per_quarter

# Track info
class MidiTrackInfo:

    def __init__(self, name: str = None, channel: int = -1):
        super().__init__()
        self.name = name
        self.channel = channel

# Track events
class MidiTrackEvent:

    def __init__(self, timecode: int = 0, message: MidiMessage = None):
        super().__init__()
        self.timecode = timecode
        self.message = message

# The result from a message processor
class MidiMessageResult:
    """Midi message processing result"""
    SKIPPED = 0     # No action taken
    HANDLED = 1     # Action taken
    TERMINATE = 2   # Do not continue propogation

# A processing protocol for processing midi messages
class MidiMessageProcessor:
    def map(self, timecode: int, message:MidiMessage) -> MidiMessageResult:
        ...
