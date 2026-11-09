"""
Animacy

Audio playback behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.behavior.base import Behavior
from animacy.contracts.driver import AudioDriverValue, DriverTransition
from animacy.contracts.midi import MidiMessage, MidiMessageResult
from animacy.contracts.performance import (
    PerformanceDataMessage,
    PerformanceEvent,
    PerformanceLoadSongMessage,
    PerformanceMessage,
    PerformanceMessageResult,
    PerformanceResetEventMessage,
    PerformanceSongContinueMessage,
    PerformanceSongPositionMessage,
    PerformanceSongStartMessage,
    PerformanceSongStopMessage,
    PerformanceVolumeMessage,
)
from animacy.curves.instant import InstantCurve
from animacy.drivers.audio import AudioDriver
from animacy.utils.logging import INFO, CatalogLogger

logger = CatalogLogger(__name__)


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

    def map(self, timecode: int, message: MidiMessage) -> MidiMessageResult:
        return MidiMessageResult.SKIPPED

    def process(self, message: PerformanceMessage) -> PerformanceMessageResult:
        """Process performance events."""
        logger.log(1, INFO, message.id, message.timecode)
        if isinstance(message, PerformanceResetEventMessage):
            logger.log(1002, INFO, message.id, message.timecode)
            self._update(message=message, command="STOP")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceLoadSongMessage):
            logger.log(1003, INFO, message.id, message.timecode, message.song)
            self._update(message=message, command=f"LOAD {message.song}.wav")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongStartMessage):
            logger.log(3, INFO, message.id, message.timecode)
            self._update(message=message, command="START")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongStopMessage):
            logger.log(4, INFO, message.id, message.timecode)
            self._update(message=message, command="STOP")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongContinueMessage):
            logger.log(1006, INFO, message.id, message.timecode)
            return PerformanceMessageResult.SKIPPED
        elif isinstance(message, PerformanceSongPositionMessage):
            logger.log(1007, INFO, message.id, message.timecode)
            return PerformanceMessageResult.SKIPPED
        elif isinstance(message, PerformanceVolumeMessage):
            logger.log(1008, INFO, message.id, message.timecode)
            return PerformanceMessageResult.SKIPPED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message: PerformanceDataMessage, command: str) -> None:
        """Update the driver with a command."""
        song_transition = DriverTransition(
            self.driver, AudioDriverValue(command), AudioDriverValue(command)
        )
        message.events.append(
            PerformanceEvent(
                transition=song_transition,
                curve=InstantCurve(),
                start=message.timecode,
                end=message.timecode,
            )
        )
        logger.log(1009, INFO, command, message.timecode)
