
"""
DaBones

Show contracts.

Copyright (c) 2026 Sparky Bobo
"""

from dabones.behavior.base import *
from dabones.contracts.midi import *
from dabones.contracts.planner import *
from dabones.contracts.service import *
from dabones.contracts.show import *

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

    def add_service(self, service: Service) -> None:
        ...

    def add_behavior(self, behavior: Behavior) -> None:
        ...

    def add_mapping(self, mapping: MidiMessageProcessor) -> None:
        ...

    @property
    def status(self) -> ShowStatus:        
        ...

    @property
    def planner_cache(self) -> DriverValueCache:        
        raise NotImplementedError

    @property
    def planner_queue(self) -> PerformanceMessageProcessor:        
        raise NotImplementedError
