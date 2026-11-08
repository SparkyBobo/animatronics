"""
Animacy

Message definitions for messages not defined by adafruit.
These are used internally with the adafruit framework, they
are not contracts for the Animacy MIDI layer.

Copyright (c) 2026 Sparky Bobo
"""

from adafruit_midi.midi_message import MIDIMessage
from adafruit_midi.system_exclusive import SystemExclusive

# System Common Messages
# Song Select
class SongSelect(MIDIMessage):
    """Song select message."""
    _STATUS = 0xF1
    _STATUSMASK = 0xFF
    LENGTH = 2     

    def __init__(self, id) -> None:
        """Initialize SongSelect."""
        super().__init__(channel=None)
        self.id = id

    def __bytes__(self):
        return bytes([self._STATUS, self.id])

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(msg_bytes[1])

SongSelect.register_message_type()                

# Song Position
class SongPosition(MIDIMessage):
    """Song position message."""
    _STATUS = 0b11110010
    _STATUSMASK = 0xFF
    LENGTH = 3

    def __init__(self, position) -> None:
        """Initialize SongPosition."""
        super().__init__(channel=None)
        self.position = position

    def __bytes__(self):
        byte1 = self.position & 0x7F
        byte2 = self.position >> 7
        return bytes([self._STATUS, byte1, byte2])

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(msg_bytes[1], msg_bytes[2])

SongPosition.register_message_type()                

# Tune Request
class TuneRequest(MIDIMessage):
    """Tune request message."""
    _STATUS = 0b11110110
    _STATUSMASK = 0xFF
    LENGTH = 1

    def __init__(self) -> None:
        """Initialize TuneRequest."""
        super().__init__(channel=None)

    def __bytes__(self):
        return bytes([self._STATUS])

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls()

TuneRequest.register_message_type()                

# System Exclusive
# No need to register, already parsed by system exclusive.
# Universal System command
class UniversalSystem(SystemExclusive):
    """SysEx universal message."""
    def __init__(self, channel: int, sub1: int, sub2: int, data:bytes, manufacturer_id=0x7e):
        """Initialize MidiUniversalSystem."""
        super().__init__(channel=channel)
        self.manufacturer_id = manufacturer_id
        self.sub1 = sub1
        self.sub2 = sub2
        self.data = data

    def __bytes__(self):
        return bytes([
            self._STATUS, 
            self.manufacturer_id, 
            self.sub1, 
            self.sub2, 
            self.data, 
            self.END_STATUS
        ])

    @classmethod
    def from_bytes(cls, msg_bytes):
        manufacturer_id = msg_bytes[0]
        return UniversalSystem.from_data_bytes(msg_bytes[1:])

    @classmethod
    def from_sysex_bytes(cls, msg_bytes, manufacturer_id=0x7e):
        channel = msg_bytes[0]
        sub1 = msg_bytes[1]
        sub2 = msg_bytes[2]
        data = msg_bytes[3:]
        return cls(channel, sub1, sub2, data)     

# File Commands
class FileHeader(UniversalSystem):
    """SysEx universal file header message."""
    def __init__(self, channel:int, len:int, name:str):
        """Initialize FileHeader."""
        self.channel = channel
        self.length = len
        self.name = name
        len1 = len >> 21 & 0x7f
        len2 = len >> 14 & 0x7f
        len3 = len >> 7 & 0x7f
        len4 = len & 0x7f
        sysex_data = bytes(['M', 'I', 'D', 'I', len1, len2, len3, len4]) + name
        super().__init__(manufacturer_id=0x7e, channel=channel, sub1=0x07, sub2=0x01, data=sysex_data)

    @classmethod
    def from_sysex_bytes(cls, channel:int, msg_bytes):
        # msg_bytes[0:3] is "MIDI"
        length = msg_bytes[4] << 21 + msg_bytes[5] << 14 + msg_bytes[6] << 7 + msg_bytes[7]
        name = str(msg_bytes[8:])
        return cls(channel, length, name)        

class FileContent(UniversalSystem):
    """SysEx universal file header message."""
    def __init__(self, channel:int, data:bytes):
        """Initialize FileHeader."""
        self.channel = channel
        self.data = data
        encoded_data = FileContent._encode_file_bytes(data)
        super().__init__(manufacturer_id=0x7e, channel=channel, sub1=0x07, sub2=0x01, data=encoded_data)

    @classmethod
    def from_sysex_bytes(cls, channel:int, msg_bytes):
        decoded_data = FileContent._decode_file_bytes(msg_bytes)
        return cls(channel, decoded_data)         

    @classmethod
    def _encode_file_bytes(cls, data:bytes) -> bytearray:
        """Write the 8-bit byte array as a sysex buffer, not including the terminator."""
        result = bytearray()
        for offset in range(0, len(data), 8):
            data[offset] = 0
            for i, value in enumerate(data[offset + 1:offset + 7]):
                if (value & 0x80):
                    data[offset] += 1 << i
                result.append(value)
        return result

    @classmethod
    def _decode_file_buffer(cls,  data:bytes) -> bytearray:
        """Parse the sysex buffer as an 8-bit byte array, not including the terminator."""
        # Each set of 7 file-bytes (represented in binary here) with the Most Significant Bits stripped
        # off and sent separately, packed into the first byte.
        result = bytearray()
        for offset in range(0, len(data), 8):
            msbs = data[offset]
            for i, value in enumerate(data[offset + 1:offset + 8]):
                if msbs & (1 << i):
                    value |= 0x80
                result.append(value)
        return result

# File open
class FileOpen(UniversalSystem):
    """SysEx universal file open message."""
    def __init__(self, channel:int, id:int):
        """Initialize FileOpen."""
        self.id = id
        id1 = id >> 7 & 0x7f
        id2 = id & 0x7f
        sysex_data = bytes([id1, id2])
        super().__init__(manufacturer_id=0x7e, channel=channel, sub1=0x0b, sub2=0x01, data=sysex_data)

    @classmethod
    def from_sysex_bytes(cls, channel:int, msg_bytes):
        id = msg_bytes[0] << 7 + msg_bytes[1]
        return cls(channel, id) 

# Volume
class VolumeSet(UniversalSystem):
    """SysEx universal volume message."""
    def __init__(self, channel:int, level:int):
        """Initialize Volume."""
        self.level = level
        lvl1 = len >> 7 & 0x7f
        lvl2 = len & 0x7f
        sysex_data = bytes([lvl1, lvl2])
        super().__init__(manufacturer_id=0x7f, channel=channel, sub1=0x04, sub2=0x01, data=sysex_data)

    @classmethod
    def from_data_bytes(cls, channel:int, msg_bytes):
        level = msg_bytes[0] << 7 + msg_bytes[1]
        return cls(channel, level)     

                
