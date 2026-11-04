"""
DaBones

Show contracts.

Copyright (c) 2026 Sparky Bobo
"""

import dabones.behavior.base
import dabones.contracts.midi
import dabones.contracts.performance
import dabones.contracts.planner
import dabones.contracts.service

# A protocol for the show status
class ShowStatus:
    @property
    def is_running(self) -> bool:
        ...

    @property
    def show_clock(self) -> int:
        ...

    @property
    def start_clock(self) -> int:
        ...

    @property
    def next_clock_tick(self) -> int:
        ...

# A protocol for the show context
class ShowContext:
    def run(self) -> None:
        ...

    def add_service(self, service: dabones.contracts.service.Service) -> None:
        ...

    def add_behavior(self, behavior: dabones.behavior.base.Behavior) -> None:
        ...

    def add_mapping(self, mapping: dabones.contracts.midi.MidiMessageProcessor) -> None:
        ...

    @property
    def status(self) -> ShowStatus:
        ...

    @property
    def planner_cache(self) -> dabones.contracts.planner.DriverValueCache:
        raise NotImplementedError

    @property
    def planner_queue(self) -> dabones.contracts.performance.PerformanceMessageProcessor:
        raise NotImplementedError
