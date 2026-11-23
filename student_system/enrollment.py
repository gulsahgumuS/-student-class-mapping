"""Enrollment: association class between Student and Course."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .course import Course
    from .student import Student

GRADE_POINTS = {
    "AA": 4.0,
    "BA": 3.5,
    "BB": 3.0,
    "CB": 2.5,
    "CC": 2.0,
    "DC": 1.5,
    "DD": 1.0,
    "FF": 0.0,
}


class Enrollment:
    def __init__(self, student: Student, course: Course, semester: str) -> None:
        self.student = student
        self.course = course
        self.semester = semester
        self.enrolled_on = date.today()
        self._grade: Optional[str] = None

    @property
    def grade(self) -> Optional[str]:
        return self._grade

    def assign_grade(self, grade: str) -> None:
        normalized = grade.upper()
        if normalized not in GRADE_POINTS:
            raise ValueError(f"invalid grade: {grade}")
        self._grade = normalized

    def grade_points(self) -> Optional[float]:
        return None if self._grade is None else GRADE_POINTS[self._grade]
