"""Transcript: builds a student's academic report."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .student import Student


class Transcript:
    def __init__(self, student: Student) -> None:
        self.student = student

    def render(self) -> str:
        student = self.student
        lines = [
            f"Transcript: {student.name} ({student.student_number})",
            f"Department: {student.department.name}",
        ]

        semesters = dict.fromkeys(e.semester for e in student.enrollments)
        for semester in semesters:
            lines.append(f"\n{semester}")
            for e in student.enrollments:
                if e.semester == semester:
                    grade = e.grade.name if e.grade else "--"
                    lines.append(
                        f"  {e.course.code:<15}{e.course.title:<32}"
                        f"{e.course.credits:>2} cr  {grade:<3}{e.status.value}"
                    )
            lines.append(f"  Semester GPA: {self._gpa_text(semester)}")

        lines.append(f"\nCumulative GPA: {self._gpa_text()}")
        lines.append(f"Earned credits: {student.earned_credits()}")
        return "\n".join(lines)

    def _gpa_text(self, semester: Optional[str] = None) -> str:
        has_grade = any(
            e.grade is not None and (semester is None or e.semester == semester)
            for e in self.student.enrollments
        )
        return f"{self.student.calculate_gpa(semester):.2f}" if has_grade else "N/A"
