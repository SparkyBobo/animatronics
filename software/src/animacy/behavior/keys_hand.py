"""
Animacy

Keys hand behaviors.

Copyright (c) 2026 Sparky Bobo
"""


from animacy.behavior.base import Behavior
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.midi import (
    MidiMessage,
    MidiMessageResult,
    MidiNoteOff,
    MidiNoteOn,
    MidiPitchBend,
)
from animacy.contracts.performance import (
    PerformanceDataMessage,
    PerformanceEvent,
    PerformanceMessageProcessor,
    PerformanceMessageResult,
    PerformancePlayTechiqueMessage,
    PerformanceResetEventMessage,
)
from animacy.contracts.planner import DriverValueCache
from animacy.contracts.setpoint import Setpoint
from animacy.curves.ease import ZeroEndpointAccelerationCurve
from animacy.drivers.servo import ServoDriver
from animacy.hardware.ports import IOPort



class KeysHandBehavior(Behavior):
    """Keys hand behaviors."""

    def __init__(
        self,
        updown: IOPort,
        slide: IOPort,
        start_note: int,
        end_note: int,
        next: PerformanceMessageProcessor,
        cache: DriverValueCache,
        name: str = "KeysHand",
    ) -> None:
        """Initialize KeysHandBehavior."""
        super().__init__(name)
        self.updown = ServoDriver(updown)
        self.slide = ServoDriver(slide)
        self.start_note = start_note
        self.end_note = end_note
        self.next = next
        self.cache = cache

        # Keys hand has a few setpoints: strike (@surface), attack (@apex), soft attack (half way), low, and high
        self.setpoints = [
            Setpoint("attack", PositionDriverValue(1400)),
            Setpoint("soft", PositionDriverValue(1550)),
            Setpoint("strike", PositionDriverValue(1700)),
            Setpoint("low", PositionDriverValue(1300)),
            Setpoint("mid", PositionDriverValue(1750)),
            Setpoint("high", PositionDriverValue(2000)),
        ]

    def map(self, timecode: int, message: MidiMessage) -> MidiMessageResult:
        if (
            isinstance(message, MidiNoteOn)
            and message.note >= self.start_note
            and message.note <= self.end_note
        ):
            self.next.process(
                PerformancePlayTechiqueMessage(
                    timecode=timecode,
                    technique=message.note - self.start_note,
                    intensity=message.velocity,
                )
            )
            return MidiMessageResult.HANDLED
        if (
            isinstance(message, MidiNoteOff)
            and message.note >= self.start_note
            and message.note <= self.end_note
        ):
            return MidiMessageResult.HANDLED
        if isinstance(message, MidiPitchBend):
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED

    def process(self, message: PerformanceDataMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            self._update(message, position=0)
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformancePlayTechiqueMessage):
            self._update(message, position=message.technique)
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def _update(self, message: PerformanceDataMessage, position: int) -> None:
        """Update the driver with a command."""
        slide_progress = (position * 1.0) / ((self.end_note - self.start_note) * 1.0)
        slide_position = self.setpoints[3].value.interpolate(
            self.setpoints[5].value, slide_progress
        )
        slide_prep_transition = DriverTransition(
            self.slide, slide_position, slide_position
        )
        prep_transition = DriverTransition(
            self.updown, self.setpoints[0].value, self.setpoints[0].value
        )
        play_transition = DriverTransition(
            self.updown, self.setpoints[0].value, self.setpoints[2].value
        )

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(
            slide_prep_transition
        )
        slide_prep_transition.start_value = (
            position_last_value or self.setpoints[2].value
        )

        (position_last_value, position_last_time) = self.cache.get(prep_transition)
        prep_transition.start_value = position_last_value or self.setpoints[2].value

        # Decide how much time we need
        prep_timecode = 24
        play_timecode = 6
        target_start = max(message.timecode - prep_timecode, position_last_time)
        target_play = max(message.timecode - play_timecode, target_start)

        # Move to the string start, then play through to end string.
        message.events.append(
            PerformanceEvent(
                transition=slide_prep_transition,
                curve=ZeroEndpointAccelerationCurve(),
                start=target_start,
                end=target_play,
            )
        )
        message.events.append(
            PerformanceEvent(
                transition=prep_transition,
                curve=ZeroEndpointAccelerationCurve(),
                start=target_start,
                end=target_play,
            )
        )
        message.events.append(
            PerformanceEvent(
                transition=play_transition,
                curve=ZeroEndpointAccelerationCurve(),
                start=target_play,
                end=message.timecode,
            )
        )
        message.timecode = target_play
        # logger.info(f"Key transition to {position}@{message.timecode}")
