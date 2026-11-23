"""Enrollment: association class between Student and Course."""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, Optional

from .exceptions import InvalidGradeError

if TYPE_CHECKING:
    from .course import Course
    from .student import Student


class Grade(Enum):
    AA = 4.0
    BA = 3.5
    BB = 3.0
    CB = 2.5
    CC = 2.0
    DC = 1.5
    DD = 1.0
    FF = 0.0

    @property
    def points(self) -> float:
        return self.value

    @property
    def is_passing(self) -> bool:
        return self is not Grade.FF

    @classmethod
    def parse(cls, text: str) -> Grade:
        try:
            return cls[text.strip().upper()]
        except KeyError:
            raise InvalidGradeError(f"invalid grade: {text}") from None


class EnrollmentStatus(Enum):
    ACTIVE = "Active"
    PASSED = "Passed"
    FAILED = "Failed"


class Enrollment:
    def __init__(self, student: Student, course: Course, semester: str) -> None:
        self.student = student
        self.course = course
        self.semester = semester
        self.enrolled_on = date.today()
        self._grade: Optional[Grade] = None

    @property
    def grade(self) -> Optional[Grade]:
        return self._grade

    @property
    def status(self) -> EnrollmentStatus:
        if self._grade is None:
            return EnrollmentStatus.ACTIVE
        return EnrollmentStatus.PASSED if self._grade.is_passing else EnrollmentStatus.FAILED

    def assign_grade(self, grade: str) -> None:
        self._grade = Grade.parse(grade)

    def grade_points(self) -> Optional[float]:
        return None if self._grade is None else self._grade.points
