"""Student: inherits from Person and enrolls in courses."""

from __future__ import annotations

from typing import Optional

from .course import Course
from .department import Department
from .enrollment import Enrollment
from .person import Person


class Student(Person):
    def __init__(
        self,
        person_id: str,
        name: str,
        email: str,
        student_number: str,
        department: Department,
    ) -> None:
        super().__init__(person_id, name, email)
        self.student_number = student_number
        self.department = department
        self._enrollments: list[Enrollment] = []
        department.add_student(self)

    @property
    def enrollments(self) -> tuple[Enrollment, ...]:
        return tuple(self._enrollments)

    def get_role(self) -> str:
        return "Student"

    def enroll(self, course: Course, semester: str) -> Enrollment:
        if self._find_enrollment(course, semester) is not None:
            raise ValueError(f"already enrolled in {course.code} for {semester}")

        enrollment = Enrollment(self, course, semester)
        course.add_enrollment(enrollment)
        self._enrollments.append(enrollment)
        return enrollment

    def drop(self, course: Course, semester: str) -> None:
        enrollment = self._require_enrollment(course, semester)
        course.remove_enrollment(enrollment)
        self._enrollments.remove(enrollment)

    def assign_grade(self, course: Course, semester: str, grade: str) -> None:
        self._require_enrollment(course, semester).assign_grade(grade)

    def calculate_gpa(self) -> float:
        graded = [e for e in self._enrollments if e.grade is not None]
        total_credits = sum(e.course.credits for e in graded)
        if total_credits == 0:
            return 0.0

        total_points = sum(e.grade_points() * e.course.credits for e in graded)
        return round(total_points / total_credits, 2)

    def _find_enrollment(self, course: Course, semester: str) -> Optional[Enrollment]:
        for enrollment in self._enrollments:
            if enrollment.course is course and enrollment.semester == semester:
                return enrollment
        return None

    def _require_enrollment(self, course: Course, semester: str) -> Enrollment:
        enrollment = self._find_enrollment(course, semester)
        if enrollment is None:
            raise ValueError(f"not enrolled in {course.code} for {semester}")
        return enrollment
