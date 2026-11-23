"""Department: aggregates students and courses."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .course import Course
    from .student import Student


class Department:
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name
        self._students: list[Student] = []
        self._courses: list[Course] = []

    @property
    def students(self) -> tuple[Student, ...]:
        return tuple(self._students)

    @property
    def courses(self) -> tuple[Course, ...]:
        return tuple(self._courses)

    def add_student(self, student: Student) -> None:
        if student not in self._students:
            self._students.append(student)

    def add_course(self, course: Course) -> None:
        if course not in self._courses:
            self._courses.append(course)
