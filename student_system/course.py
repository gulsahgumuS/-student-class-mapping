"""Course: a class that students can enroll in."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .enrollment import Enrollment


class Course:
    def __init__(self, code: str, title: str, credits: int, capacity: int) -> None:
        if credits <= 0:
            raise ValueError("credits must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.code = code
        self.title = title
        self.credits = credits
        self.capacity = capacity
        self._enrollments: list[Enrollment] = []

    @property
    def enrollments(self) -> tuple[Enrollment, ...]:
        return tuple(self._enrollments)

    def is_full(self) -> bool:
        return len(self._enrollments) >= self.capacity

    def add_enrollment(self, enrollment: Enrollment) -> None:
        if self.is_full():
            raise ValueError(f"{self.code} is full")
        self._enrollments.append(enrollment)

    def remove_enrollment(self, enrollment: Enrollment) -> None:
        self._enrollments.remove(enrollment)
