"""
Animacy

Audio playback behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.contracts.midi import *
from animacy.contracts.driver import *
from animacy.contracts.performance import *
from animacy.behavior.base import Behavior
from animacy.drivers.audio import AudioDriver
from animacy.curves.instant import InstantCurve

from animacy.utils.logging import INFO, log

class AudioBehavior(Behavior):
    """Audio playback behaviors."""

    def __init__(
        self,
        driver: AudioDriver,
        name: str,
    ) -> None:
        """Initialize AudioBehavior."""
        super().__init__(name)
        self.driver = driver

    def map(self, timecode:int, message:MidiMessage) -> MidiMessageResult:
        return MidiMessageResult.SKIPPED        

    def process(self, message:PerformanceMessage) -> PerformanceMessageResult:
        """Process performance events."""
        log(1, INFO, message.id, message.timecode)
        if isinstance(message, PerformanceResetEventMessage) or isinstance(message, PerformanceResetEventMessage):
            log(1002, INFO, message.id, message.timecode)
            self._update(message=message, command="STOP")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceLoadSongMessage):
            log(1003, INFO, message.id, message.timecode, message.song)
            self._update(message=message, command=f"LOAD {message.song}.wav")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongStartMessage):
            log(3, INFO, message.id, message.timecode)
            self._update(message=message, command="START")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongStopMessage):
            log(4, INFO, message.id, message.timecode)
            self._update(message=message, command="STOP")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongContinueMessage):
            log(1006, INFO, message.id, message.timecode)
            return PerformanceMessageResult.SKIPPED
        elif isinstance(message, PerformanceSongPositionMessage):
            log(1007, INFO, message.id, message.timecode)
            return PerformanceMessageResult.SKIPPED
        elif isinstance(message, PerformanceVolumeMessage):
            log(1008, INFO, message.id, message.timecode)
            return PerformanceMessageResult.SKIPPED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message:PerformanceDataMessage, command: str) -> None:
        """Update the driver with a command."""
        song_transition = DriverTransition(self.driver, AudioDriverValue(command), AudioDriverValue(command))
        message.events.append(PerformanceEvent(transition=song_transition, curve=InstantCurve(), start=message.timecode, end=message.timecode))
        log(1009, INFO, command, message.timecode)
