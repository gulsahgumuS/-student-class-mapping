"""Instructor: inherits from Person, teaches courses, and submits grades."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .person import Person

if TYPE_CHECKING:
    from .course import Course
    from .department import Department
    from .student import Student


class Instructor(Person):
    def __init__(self, person_id: str, name: str, email: str, department: Department) -> None:
        super().__init__(person_id, name, email)
        self.department = department
        self.courses: list[Course] = []
        department.instructors.append(self)

    def get_role(self) -> str:
        return "Instructor"

    def assign_course(self, course: Course) -> None:
        if course.instructor not in (None, self):
            raise ValueError(f"{course.code} already has an instructor")
        course.instructor = self
        if course not in self.courses:
            self.courses.append(course)

    def submit_grade(self, student: Student, course: Course, semester: str, grade: str) -> None:
        if course.instructor is not self:
            raise ValueError(f"{self.name} does not teach {course.code}")
        student.assign_grade(course, semester, grade)
