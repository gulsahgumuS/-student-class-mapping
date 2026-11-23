"""Course: a class that students can enroll in."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional

from .exceptions import CourseFullError

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from .instructor import Instructor


class Course:
    def __init__(
        self,
        code: str,
        title: str,
        credits: int,
        capacity: int,
        prerequisites: Iterable[Course] = (),
    ) -> None:
        if credits <= 0:
            raise ValueError("credits must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.code = code
        self.title = title
        self.credits = credits
        self.capacity = capacity
        self.instructor: Optional[Instructor] = None
        self._prerequisites = tuple(prerequisites)
        self._enrollments: list[Enrollment] = []

    @property
    def prerequisites(self) -> tuple[Course, ...]:
        return self._prerequisites

    @property
    def enrollments(self) -> tuple[Enrollment, ...]:
        return tuple(self._enrollments)

    def is_full(self, semester: str) -> bool:
        taken = sum(1 for e in self._enrollments if e.semester == semester)
        return taken >= self.capacity

    def add_enrollment(self, enrollment: Enrollment) -> None:
        if self.is_full(enrollment.semester):
            raise CourseFullError(f"{self.code} is full for {enrollment.semester}")
        self._enrollments.append(enrollment)

    def remove_enrollment(self, enrollment: Enrollment) -> None:
        self._enrollments.remove(enrollment)
