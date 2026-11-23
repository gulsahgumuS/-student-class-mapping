"""Student: inherits from Person and enrolls in courses."""

from __future__ import annotations

from typing import Optional

from .course import Course
from .department import Department
from .enrollment import Enrollment, EnrollmentStatus
from .exceptions import (
    CreditLimitError,
    DuplicateEnrollmentError,
    EnrollmentError,
    PrerequisiteError,
)
from .person import Person
from .transcript import Transcript


class Student(Person):
    MAX_SEMESTER_CREDITS = 30

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
        self._check_can_enroll(course, semester)
        enrollment = Enrollment(self, course, semester)
        course.add_enrollment(enrollment)
        self._enrollments.append(enrollment)
        return enrollment

    def drop(self, course: Course, semester: str) -> None:
        enrollment = self._require_enrollment(course, semester)
        if enrollment.grade is not None:
            raise EnrollmentError(f"cannot drop graded course {course.code}")
        course.remove_enrollment(enrollment)
        self._enrollments.remove(enrollment)

    def assign_grade(self, course: Course, semester: str, grade: str) -> None:
        self._require_enrollment(course, semester).assign_grade(grade)

    def passed_courses(self) -> set[Course]:
        return {e.course for e in self._enrollments if e.status is EnrollmentStatus.PASSED}

    def earned_credits(self) -> int:
        return sum(course.credits for course in self.passed_courses())

    def semester_credits(self, semester: str) -> int:
        return sum(e.course.credits for e in self._enrollments if e.semester == semester)

    def calculate_gpa(self, semester: Optional[str] = None) -> float:
        """Credit-weighted GPA. For retaken courses, only the latest grade counts."""
        graded = [
            e for e in self._enrollments
            if e.grade is not None and (semester is None or e.semester == semester)
        ]
        latest = {e.course: e for e in graded}.values()
        total_credits = sum(e.course.credits for e in latest)
        if total_credits == 0:
            return 0.0

        total_points = sum(e.grade_points() * e.course.credits for e in latest)
        return round(total_points / total_credits, 2)

    def transcript(self) -> Transcript:
        return Transcript(self)

    def _check_can_enroll(self, course: Course, semester: str) -> None:
        if self._find_enrollment(course, semester) is not None:
            raise DuplicateEnrollmentError(f"already enrolled in {course.code} for {semester}")

        passed = self.passed_courses()
        if course in passed:
            raise DuplicateEnrollmentError(f"already passed {course.code}")

        missing = [p.code for p in course.prerequisites if p not in passed]
        if missing:
            raise PrerequisiteError(f"{course.code} requires: {', '.join(missing)}")

        if self.semester_credits(semester) + course.credits > self.MAX_SEMESTER_CREDITS:
            raise CreditLimitError(f"credit limit exceeded for {semester}")

    def _find_enrollment(self, course: Course, semester: str) -> Optional[Enrollment]:
        for enrollment in self._enrollments:
            if enrollment.course is course and enrollment.semester == semester:
                return enrollment
        return None

    def _require_enrollment(self, course: Course, semester: str) -> Enrollment:
        enrollment = self._find_enrollment(course, semester)
        if enrollment is None:
            raise EnrollmentError(f"not enrolled in {course.code} for {semester}")
        return enrollment
