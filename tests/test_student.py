import unittest

from student_system import (
    Course,
    CourseFullError,
    CreditLimitError,
    Department,
    DuplicateEnrollmentError,
    EnrollmentError,
    EnrollmentStatus,
    Instructor,
    InvalidGradeError,
    NotCourseInstructorError,
    Person,
    PrerequisiteError,
    Student,
)

FALL = "2025-Fall"
SPRING = "2026-Spring"


class StudentSystemTests(unittest.TestCase):
    def setUp(self):
        self.department = Department("SE", "Software Engineering")
        self.course = Course("SE301", "Software Design", 3, 1)
        self.other = Course("SE302", "Database Systems", 4, 30)
        self.student = Student("P1", "Ada", "ada@example.com", "1001", self.department)
        self.teacher = Instructor("P9", "Grace", "grace@example.com", "Dr.", self.department)

    def test_inheritance_and_department_links(self):
        self.assertIsInstance(self.student, Person)
        self.assertIsInstance(self.teacher, Person)
        self.assertEqual(self.student.get_role(), "Student")
        self.assertEqual(self.teacher.get_role(), "Instructor")
        self.assertIn(self.student, self.department.students)
        self.assertIn(self.teacher, self.department.instructors)

    def test_person_is_abstract(self):
        with self.assertRaises(TypeError):
            Person("P2", "Name", "name@example.com")

    def test_enroll_links_both_sides(self):
        enrollment = self.student.enroll(self.course, FALL)
        self.assertIn(enrollment, self.student.enrollments)
        self.assertIn(enrollment, self.course.enrollments)
        self.assertIs(enrollment.status, EnrollmentStatus.ACTIVE)

    def test_duplicate_enrollment_rejected(self):
        self.student.enroll(self.other, FALL)
        with self.assertRaises(DuplicateEnrollmentError):
            self.student.enroll(self.other, FALL)

    def test_full_course_leaves_student_unchanged(self):
        self.student.enroll(self.course, FALL)
        second = Student("P2", "Lin", "lin@example.com", "1002", self.department)
        with self.assertRaises(CourseFullError):
            second.enroll(self.course, FALL)
        self.assertEqual(second.enrollments, ())

    def test_capacity_is_per_semester(self):
        self.student.enroll(self.course, FALL)
        second = Student("P2", "Lin", "lin@example.com", "1002", self.department)
        second.enroll(self.course, SPRING)
        self.assertEqual(len(self.course.enrollments), 2)

    def test_drop_removes_both_sides(self):
        self.student.enroll(self.course, FALL)
        self.student.drop(self.course, FALL)
        self.assertEqual(self.student.enrollments, ())
        self.assertEqual(self.course.enrollments, ())

    def test_graded_course_cannot_be_dropped(self):
        self.student.enroll(self.course, FALL)
        self.student.assign_grade(self.course, FALL, "BB")
        with self.assertRaises(EnrollmentError):
            self.student.drop(self.course, FALL)

    def test_prerequisite_required(self):
        advanced = Course("SE401", "Advanced Design", 3, 30, [self.other])
        with self.assertRaises(PrerequisiteError):
            self.student.enroll(advanced, FALL)
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "CC")
        self.student.enroll(advanced, SPRING)

    def test_credit_limit(self):
        heavy = Course("SE500", "Project", 28, 30)
        self.student.enroll(heavy, FALL)
        with self.assertRaises(CreditLimitError):
            self.student.enroll(self.course, FALL)

    def test_gpa_is_credit_weighted(self):
        self.student.enroll(self.course, FALL)
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.course, FALL, "AA")
        self.student.assign_grade(self.other, FALL, "BB")
        self.assertEqual(self.student.calculate_gpa(), 3.43)

    def test_retake_uses_latest_grade(self):
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "FF")
        self.student.enroll(self.other, SPRING)
        self.student.assign_grade(self.other, SPRING, "BB")
        self.assertEqual(self.student.calculate_gpa(), 3.0)
        self.assertEqual(self.student.calculate_gpa(FALL), 0.0)
        self.assertEqual(self.student.earned_credits(), 4)

    def test_passed_course_cannot_be_retaken(self):
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "DD")
        with self.assertRaises(DuplicateEnrollmentError):
            self.student.enroll(self.other, SPRING)

    def test_invalid_grade_rejected(self):
        self.student.enroll(self.course, FALL)
        with self.assertRaises(InvalidGradeError):
            self.student.assign_grade(self.course, FALL, "XX")

    def test_only_course_instructor_can_grade(self):
        self.student.enroll(self.other, FALL)
        with self.assertRaises(NotCourseInstructorError):
            self.teacher.submit_grade(self.student, self.other, FALL, "AA")
        self.teacher.assign_course(self.other)
        self.teacher.submit_grade(self.student, self.other, FALL, "AA")
        self.assertEqual(self.student.calculate_gpa(), 4.0)

    def test_transcript_contains_results(self):
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "BA")
        report = self.student.transcript().render()
        self.assertIn("SE302", report)
        self.assertIn("Cumulative GPA: 3.50", report)
        self.assertIn("Earned credits: 4", report)


if __name__ == "__main__":
    unittest.main()
