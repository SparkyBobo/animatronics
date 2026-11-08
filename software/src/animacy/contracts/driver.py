"""
Animacy

Driver command and value contracts.

Copyright (c) 2026 Sparky Bobo
"""

from __future__ import annotations
from animacy.contracts.color import Color

# A driver values base class
class DriverValue:
    """Base type for typed values sent to a driver."""

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, DriverValue)
            and type(self) is type(other)
            and self.__dict__ == other.__dict__
        )

    def components(self) -> tuple[int, ...]:
        """Return this value as ordered integer components."""
        raise NotImplementedError

    @classmethod
    def from_components(
        cls: type["DriverValue"],
        components: tuple[int, ...],
    ) -> "DriverValue":
        """Build this value type from ordered integer components."""
        raise NotImplementedError

    def interpolate(
        self: "DriverValue",
        target: "DriverValue",
        progress: float,
    ) -> "DriverValue":
        if type(target) is not type(self):
            raise TypeError("Driver values must have the same concrete type")

        start_components = self.components()
        target_components = target.components()
        if len(start_components) != len(target_components):
            raise ValueError("Driver values must have the same number of components")

        progress = min(max(progress, 0.0), 1.0)
        result_components = tuple(
            round(start + (end - start) * progress)
            for start, end in zip(start_components, target_components)
        )
        return type(self).from_components(result_components)

# A driver position value.
class PositionDriverValue(DriverValue):

    def __init__(self, position: int = 0):
        super().__init__()
        self.position = position

    def __str__(self) -> str:
        return f"PositionDriverValue({self.position})"

    def components(self) -> tuple[int, ...]:
        return (self.position,)

    @classmethod
    def from_components(
        cls,
        components: tuple[int, ...],
    ) -> PositionDriverValue:
        if len(components) != 1:
            raise ValueError("PositionDriverValue requires one component")
        return cls(position=components[0])

# A driver intensity value.
class IntensityDriverValue(DriverValue):

    def __init__(self, intensity: int = 0):
        super().__init__()
        self.intensity = intensity

    def __str__(self) -> str:
        return f"IntensityDriverValue({self.intensity})"

    def components(self) -> tuple[int, ...]:
        return (self.intensity,)

    @classmethod
    def from_components(
        cls,
        components: tuple[int, ...],
    ) -> IntensityDriverValue:
        if len(components) != 1:
            raise ValueError("IntensityDriverValue requires one component")
        return cls(intensity=components[0])

# A driver color value.
class ColorDriverValue(DriverValue):

    def __init__(self, color: Color = None):
        super().__init__()
        self.color = color

    def __str__(self) -> str:
        return f"ColorDriverValue({self.color})"

    def components(self) -> tuple[int, ...]:
        return (self.color.red, self.color.green, self.color.blue, self.color.white)

    @classmethod
    def from_components(
        cls,
        components: tuple[int, ...],
    ) -> ColorDriverValue:
        if len(components) != 4:
            raise ValueError("ColorDriverValue requires four components")
        return cls(color=Color(*components))

# An audio value.
class AudioDriverValue(DriverValue):

    def __init__(self, command: str):
        super().__init__()
        self.command = command

    def __str__(self) -> str:
        return f"AudioDriverValue({self.command})"


    def interpolate(self: AudioDriverValue, target: AudioDriverValue, progress: float) -> AudioDriverValue:
        return target

    def components(self) -> tuple[int, ...]:
        return (0,)

    @classmethod
    def from_components(
        cls,
        components: tuple[int, ...],
    ) -> AudioDriverValue:
        if len(components) != 1:
            raise ValueError("AudioDriverValue requires one component")
        return cls(command="")

# A driver transition between two values.
class DriverTransition:
    """A value transition routed to a driver without a device address."""

    def __init__(self, driver: Driver=None, start_value: DriverValue=None, end_value: DriverValue=None, progress: float = 0.0):
        super().__init__()
        self.driver = driver
        self.start_value = start_value
        self.end_value = end_value
        self.progress = progress
        if type(self.start_value) is not type(self.end_value):
            raise TypeError("Transition values must have the same concrete type")

    @property
    def id(self) -> str:
        return f"{self.key}:{self.start_value}:{self.end_value}"

    @property
    def key(self) -> str:
        return f"{id(self.driver)}:{type(self.end_value).__name__}"

# A driver transition with an address.
class AddressableDriverTransition(DriverTransition):
    """A driver transition addressed to one device on a bus."""

    def __init__(self, driver: Driver=None, start_value: DriverValue=None, end_value: DriverValue=None, progress: float = 0.0, address: int = -1):
        super().__init__(driver, start_value, end_value, progress)
        self.address = address

    @property
    def key(self) -> str:
        return f"{id(self.driver)}:{self.address}:{type(self.end_value).__name__}"

# A transition result
class DriverTransitionResult:
    """Driver transition processing result."""
    SKIPPED = 0         # No action taken
    EXECUTED = 201      # Action taken
    CONSTRAINED = 202   # Action constrained by driver limit

# Constraints for a driver.
class DriverConstraints:
    """Bounds and motion limits for a driver value.

    Bounds must use the same DriverValue subtype as the queried value. None
    means that the corresponding constraint is unbounded.
    """

    def __init__(self, minimum: DriverValue = None, maximum: DriverValue = None, max_velocity: float = None, max_acceleration: float = None):
        super().__init__()
        self.minimum = minimum
        self.maximum = maximum
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration

# The driver processing protocol.
class Driver():
    def process(self, transition: DriverTransition) -> DriverTransitionResult:
        ...

    def constraints_for(self, value: DriverValue) -> DriverConstraints:
        """Return constraints for the given typed driver value."""
        ...
