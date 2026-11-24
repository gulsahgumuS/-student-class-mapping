"""Course: a class that students can enroll in."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from .instructor import Instructor


class Course:
    def __init__(
        self,
        code: str,
        title: str = "",
        credits: int = 3,
        capacity: int = 30,
        prerequisites: Iterable[Course] = (),
    ) -> None:
        if credits <= 0 or capacity <= 0:
            raise ValueError("credits and capacity must be positive")

        self.code = code
        self.title = title
        self.credits = credits
        self.capacity = capacity
        self.prerequisites = tuple(prerequisites)
        self.instructor: Optional[Instructor] = None
        self.enrollments: list[Enrollment] = []

    def is_full(self, semester: str) -> bool:
        taken = sum(1 for e in self.enrollments if e.semester == semester)
        return taken >= self.capacity
