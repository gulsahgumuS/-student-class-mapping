"""Department: aggregates students, instructors, and courses."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .course import Course
    from .instructor import Instructor
    from .student import Student


class Department:
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name
        self.students: list[Student] = []
        self.instructors: list[Instructor] = []
        self.courses: list[Course] = []

    def add_course(self, course: Course) -> None:
        if course not in self.courses:
            self.courses.append(course)
