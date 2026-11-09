"""
Animacy

Pluck hand behaviors.

Copyright (c) 2026 Sparky Bobo
"""


from animacy.behavior.base import Behavior
from animacy.contracts.driver import DriverTransition, PositionDriverValue
from animacy.contracts.midi import (
    MidiMessage,
    MidiMessageResult,
    MidiNoteOff,
    MidiNoteOn,
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
from animacy.curves.ease import EaseInOutTransform
from animacy.drivers.servo import ServoDriver
from animacy.hardware.ports import IOPort



class PluckHandBehavior(Behavior):
    """Pluck hand behaviors."""

    def __init__(
        self,
        primary: IOPort,
        secondary: IOPort,
        next: PerformanceMessageProcessor,
        cache: DriverValueCache,
        name: str = "PluckHand",
    ) -> None:
        """Initialize PluckHandBehavior."""
        super().__init__(name)
        self.primary = ServoDriver(primary)
        self.secondary = ServoDriver(secondary)
        self.next = next
        self.cache = cache
        self.last_technique = 2  # force to start alternate on index finger

        # Strum hand has a few setpoints: strike (@string) and attack (@apex) for primary and secondary
        self.setpoints = [
            Setpoint("attack", PositionDriverValue(2100)),
            Setpoint("strike", PositionDriverValue(1500)),
            Setpoint("attack", PositionDriverValue(1100)),
            Setpoint("strike", PositionDriverValue(1400)),
        ]

    def map(self, timecode: int, message: MidiMessage) -> MidiMessageResult:
        if (
            isinstance(message, MidiNoteOn)
            and message.note >= 42
            and message.note <= 44
        ):
            self.next.process(
                PerformancePlayTechiqueMessage(
                    timecode=timecode,
                    technique=message.note - 42,
                    intensity=message.velocity,
                )
            )
            return MidiMessageResult.HANDLED
        if (
            isinstance(message, MidiNoteOff)
            and message.note >= 42
            and message.note <= 44
        ):
            return MidiMessageResult.HANDLED
        return MidiMessageResult.SKIPPED

    def process(self, message: PerformanceDataMessage) -> PerformanceMessageResult:
        if isinstance(message, PerformanceResetEventMessage):
            # Rest fingers on strings.
            self._update(
                message=message,
                driver=self.primary,
                attack=self.setpoints[1].value,
                strike=self.setpoints[1].value,
            )
            self._update(
                message=message,
                driver=self.secondary,
                attack=self.setpoints[3].value,
                strike=self.setpoints[3].value,
            )
            self.last_technique = 2  # force to start alternate on index finger
            return PerformanceMessageResult.HANDLED
        if isinstance(message, PerformancePlayTechiqueMessage):
            # Pick a finger: 0=index, 2=ring, 1=alternate
            self.last_technique = (
                message.technique
                if message.technique != 1
                else 0
                if self.last_technique == 2
                else 2
            )
            driver = self.primary if self.last_technique == 0 else self.secondary
            # logger.critical(f"Plucking with technique {self.last_technique}")
            self._update(
                message=message,
                driver=driver,
                attack=self.setpoints[self.last_technique].value,
                strike=self.setpoints[self.last_technique + 1].value,
            )
            return PerformanceMessageResult.HANDLED
        return PerformanceMessageResult.SKIPPED

    def _update(
        self,
        message: PerformanceDataMessage,
        driver: ServoDriver,
        attack: PositionDriverValue,
        strike: PositionDriverValue,
    ) -> None:
        """Update the driver with a command."""
        prep_transition = DriverTransition(driver, attack, attack)
        play_transition = DriverTransition(driver, attack, strike)

        # Find out where we were last.
        (position_last_value, position_last_time) = self.cache.get(prep_transition)
        prep_transition.start_value = position_last_value or strike

        # Decide how much time we need
        prep_timecode = 24
        play_timecode = 6
        target_start = max(message.timecode - prep_timecode, position_last_time)
        target_play = max(message.timecode - play_timecode, target_start)

        # Move to the attack, then play through to strike position.
        message.events.append(
            PerformanceEvent(
                transition=prep_transition,
                curve=EaseInOutTransform(),
                start=target_start,
                end=target_play,
            )
        )
        message.events.append(
            PerformanceEvent(
                transition=play_transition,
                curve=EaseInOutTransform(),
                start=target_play,
                end=message.timecode,
            )
        )
        message.timecode = target_play
        # logger.info(f"Pluck transition to {prep_transition.start_value.position} through {prep_transition.end_value.position}@{play_transition.start_value.position} target_play:{play_transition.end_value.position}")
