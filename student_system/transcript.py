"""Transcript: builds a student's academic report."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .student import Student


def _format_gpa(gpa: Optional[float]) -> str:
    return "N/A" if gpa is None else f"{gpa:.2f}"


class Transcript:
    def __init__(self, student: Student) -> None:
        self.student = student

    def render(self) -> str:
        s = self.student
        lines = [f"Transcript: {s.name} ({s.student_number})", f"Department: {s.department.name}"]

        for semester in dict.fromkeys(e.semester for e in s.enrollments):
            lines.append(f"\n{semester}")
            for e in s.enrollments:
                if e.semester == semester:
                    grade = e.grade.name if e.grade else "--"
                    lines.append(
                        f"  {e.course.code:<15}{e.course.title:<32}"
                        f"{e.course.credits:>2} cr  {grade:<3}{e.status.value}"
                    )
            lines.append(f"  Semester GPA: {_format_gpa(s.calculate_gpa(semester))}")

        lines.append(f"\nCumulative GPA: {_format_gpa(s.calculate_gpa())}")
        lines.append(f"Earned credits: {s.earned_credits()}")
        return "\n".join(lines)
