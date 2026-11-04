"""
DaBones

Audio playback behaviors.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.contracts.driver
import dabones.contracts.midi
import dabones.contracts.performance
import dabones.behavior.base
import dabones.drivers.audio
import dabones.curves.instant

import logging
logger = logging.getLogger(__name__)

class AudioBehavior(dabones.behavior.base.Behavior):
    """Audio playback behaviors."""

    def __init__(
        self,
        driver: dabones.drivers.audio.AudioDriver,
        name: str,
    ) -> None:
        """Initialize AudioBehavior."""
        super().__init__(name)
        self.driver = driver

    def map(self, timecode: int, message: dabones.contracts.midi.MidiMessage) -> dabones.contracts.midi.MidiMessageResult:
        return dabones.contracts.midi.MidiMessageResult.SKIPPED

    def process(self, message: dabones.contracts.performance.PerformanceMessage) -> dabones.contracts.performance.PerformanceMessageResult:
        """Process performance events."""
        logger.info(f"Process performance message {message.id}@{message.timecode}")
        if isinstance(message, dabones.contracts.performance.PerformanceResetEventMessage):
            logger.info(f"Process reset message {message.id}@{message.timecode}")
            self._update(message=message, command="STOP")
            return dabones.contracts.performance.PerformanceMessageResult.HANDLED
        elif isinstance(message, dabones.contracts.performance.PerformanceLoadSongMessage):
            logger.info(f"Process song load message {message.id}@{message.timecode} for song {message.song}")
            self._update(message=message, command=f"LOAD {message.song}.wav")
            return dabones.contracts.performance.PerformanceMessageResult.HANDLED
        elif isinstance(message, dabones.contracts.performance.PerformanceSongStartMessage):
            logger.info(f"Process song start message {message.id}@{message.timecode}")
            self._update(message=message, command="START")
        elif isinstance(message, dabones.contracts.performance.PerformanceSongStopMessage):
            logger.info(f"Process song stop message {message.id}@{message.timecode}")
            self._update(message=message, command="STOP")
            return dabones.contracts.performance.PerformanceMessageResult.HANDLED
        elif isinstance(message, dabones.contracts.performance.PerformanceSongContinueMessage):
            logger.info(f"Song continue not supported {message.id}@{message.timecode}")
            return dabones.contracts.performance.PerformanceMessageResult.SKIPPED
        elif isinstance(message, dabones.contracts.performance.PerformanceSongPositionMessage):
            logger.info(f"Song position not supported {message.id}@{message.timecode}")
            return dabones.contracts.performance.PerformanceMessageResult.SKIPPED
        elif isinstance(message, dabones.contracts.performance.PerformanceVolumeMessage):
            logger.info(f"Volume not suported {message.id}@{message.timecode}")
            return dabones.contracts.performance.PerformanceMessageResult.SKIPPED
        return dabones.contracts.performance.PerformanceMessageResult.SKIPPED

    def _update(self, message: dabones.contracts.performance.PerformanceDataMessage, command: str) -> None:
        """Update the driver with a command."""
        song_transition = dabones.contracts.driver.DriverTransition(
            self.driver,
            dabones.contracts.driver.AudioDriverValue(command),
            dabones.contracts.driver.AudioDriverValue(command),
        )
        message.events.append(
            dabones.contracts.performance.PerformanceEvent(
                transition=song_transition,
                curve=dabones.curves.instant.InstantCurve(),
                start=message.timecode,
                end=message.timecode,
            )
        )
        logger.info(f"Song transition to {command}@{message.timecode}")
