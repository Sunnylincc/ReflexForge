from __future__ import annotations

from reflexforge.memory.patterns import Lesson


class LessonMemory:
    def __init__(self) -> None:
        self._lessons: list[Lesson] = []

    def add(self, lesson: Lesson) -> None:
        self._lessons.append(lesson)

    def top(self, k: int = 5) -> list[Lesson]:
        return sorted(self._lessons, key=lambda l: l.confidence, reverse=True)[:k]
