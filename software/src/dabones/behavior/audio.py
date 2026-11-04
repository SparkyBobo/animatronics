"""
DaBones

Audio playback behaviors.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.contracts.midi import *
from dabones.contracts.driver import *
from dabones.contracts.performance import *
from dabones.behavior.base import Behavior
from dabones.drivers.audio import AudioDriver
from dabones.curves.instant import InstantCurve

import logging
logger = logging.getLogger(__name__)

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
        logger.info(f"Process performance message {message.id}@{message.timecode}")
        if isinstance(message, PerformanceResetEventMessage) or isinstance(message, PerformanceResetEventMessage):
            logger.info(f"Process reset message {message.id}@{message.timecode}")
            self._update(message=message, command="STOP")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceLoadSongMessage):
            logger.info(f"Process song load message {message.id}@{message.timecode} for song {message.song}")
            self._update(message=message, command=f"LOAD {message.song}.wav")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongStartMessage):
            logger.info(f"Process song start message {message.id}@{message.timecode}")
            self._update(message=message, command="START")
        elif isinstance(message, PerformanceSongStopMessage):
            logger.info(f"Process song stop message {message.id}@{message.timecode}")
            self._update(message=message, command="STOP")
            return PerformanceMessageResult.HANDLED
        elif isinstance(message, PerformanceSongContinueMessage):
            logger.info(f"Song continue not supported {message.id}@{message.timecode}")
            return PerformanceMessageResult.SKIPPED
        elif isinstance(message, PerformanceSongPositionMessage):
            logger.info(f"Song position not supported {message.id}@{message.timecode}")
            return PerformanceMessageResult.SKIPPED
        elif isinstance(message, PerformanceVolumeMessage):
            logger.info(f"Volume not suported {message.id}@{message.timecode}")
            return PerformanceMessageResult.SKIPPED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message:PerformanceDataMessage, command: str) -> None:
        """Update the driver with a command."""
        song_transition = DriverTransition(self.driver, AudioDriverValue(command), AudioDriverValue(command))
        message.events.append(PerformanceEvent(transition=song_transition, curve=InstantCurve(), start=message.timecode, end=message.timecode))
        logger.info(f"Song transition to {command}@{message.timecode}")
