"""
Animacy

Lizzie performer end-to-end tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.characters.lizzie import LizzieB
from animacy.contracts.performance import (
    PerformanceClockMessage,
    PerformanceLoadSongMessage,
    PerformanceMessage,
    PerformanceSongStartMessage,
    PerformanceSongStopMessage,
)
from animacy.contracts.service import Service, ServiceResult
from animacy.show.context import ShowContext


class ScriptedService(Service):
    def __init__(
        self, context: ShowContext, messages: list[PerformanceMessage]
    ) -> None:
        context.add_service(self)
        self.context = context
        self.messages = messages
        self.index = 0

    def service(self) -> ServiceResult:
        if self.index < len(self.messages):
            message = self.messages[self.index]
            self.index += 1
            self.context.show_dispatcher.process(message)
            return ServiceResult.ACTIVITY
        return ServiceResult.EXIT


def test_e2e_lizzie():
    messages = [
        PerformanceLoadSongMessage(song=1, timecode=-1),
        PerformanceSongStartMessage(timecode=-1),
        PerformanceClockMessage(0),
        PerformanceClockMessage(5003),
        PerformanceClockMessage(5008),
        PerformanceClockMessage(5013),
        PerformanceClockMessage(5019),
        PerformanceClockMessage(5023),
        PerformanceClockMessage(5028),
        PerformanceClockMessage(5033),
        PerformanceSongStopMessage(timecode=-1),
    ]
    context = ShowContext()
    ScriptedService(context, messages)
    LizzieB(context)
    context.run()
