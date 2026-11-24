"""Enrollment: association class between Student and Course."""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, Optional

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

    @classmethod
    def parse(cls, text: str) -> Grade:
        try:
            return cls[text.strip().upper()]
        except KeyError:
            raise ValueError(f"invalid grade: {text}") from None


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
        self.grade: Optional[Grade] = None

    @property
    def status(self) -> EnrollmentStatus:
        if self.grade is None:
            return EnrollmentStatus.ACTIVE
        return EnrollmentStatus.FAILED if self.grade is Grade.FF else EnrollmentStatus.PASSED

    def assign_grade(self, grade: str) -> None:
        self.grade = Grade.parse(grade)
