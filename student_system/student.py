"""Student: inherits from Person and enrolls in courses."""

from __future__ import annotations

from typing import Optional

from .course import Course
from .department import Department
from .enrollment import Enrollment, EnrollmentStatus
from .person import Person
from .transcript import Transcript


class Student(Person):
    MAX_SEMESTER_CREDITS = 30

    def __init__(
        self, person_id: str, name: str, email: str, student_number: str, department: Department
    ) -> None:
        super().__init__(person_id, name, email)
        self.student_number = student_number
        self.department = department
        self.enrollments: list[Enrollment] = []
        department.students.append(self)

    def get_role(self) -> str:
        return "Student"

    def enroll(self, course: Course, semester: str) -> Enrollment:
        passed = self.passed_courses()
        if self._find(course, semester) or course in passed:
            raise ValueError(f"already enrolled in or passed {course.code}")

        missing = [p.code for p in course.prerequisites if p not in passed]
        if missing:
            raise ValueError(f"{course.code} requires: {', '.join(missing)}")
        if self.semester_credits(semester) + course.credits > self.MAX_SEMESTER_CREDITS:
            raise ValueError(f"credit limit exceeded for {semester}")
        if course.is_full(semester):
            raise ValueError(f"{course.code} is full for {semester}")

        enrollment = Enrollment(self, course, semester)
        course.enrollments.append(enrollment)
        self.enrollments.append(enrollment)
        return enrollment

    def drop(self, course: Course, semester: str) -> None:
        enrollment = self._require(course, semester)
        if enrollment.grade is not None:
            raise ValueError(f"cannot drop graded course {course.code}")
        course.enrollments.remove(enrollment)
        self.enrollments.remove(enrollment)

    def assign_grade(self, course: Course, semester: str, grade: str) -> None:
        self._require(course, semester).assign_grade(grade)

    def passed_courses(self) -> set[Course]:
        return {e.course for e in self.enrollments if e.status is EnrollmentStatus.PASSED}

    def earned_credits(self) -> int:
        return sum(course.credits for course in self.passed_courses())

    def semester_credits(self, semester: str) -> int:
        return sum(e.course.credits for e in self.enrollments if e.semester == semester)

    def calculate_gpa(self, semester: Optional[str] = None) -> Optional[float]:
        """Credit-weighted GPA. For retaken courses, only the latest grade counts.
        Returns None when there are no grades yet."""
        graded = [
            e for e in self.enrollments
            if e.grade is not None and semester in (None, e.semester)
        ]
        latest = {e.course: e for e in graded}.values()
        credits = sum(e.course.credits for e in latest)
        if credits == 0:
            return None
        return round(sum(e.grade.value * e.course.credits for e in latest) / credits, 2)

    def transcript(self) -> Transcript:
        return Transcript(self)

    def _find(self, course: Course, semester: str) -> Optional[Enrollment]:
        return next(
            (e for e in self.enrollments if e.course is course and e.semester == semester), None
        )

    def _require(self, course: Course, semester: str) -> Enrollment:
        enrollment = self._find(course, semester)
        if enrollment is None:
            raise ValueError(f"not enrolled in {course.code} for {semester}")
        return enrollment
