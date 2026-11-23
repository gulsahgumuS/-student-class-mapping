import unittest

from student_system import Course, Department, Person, Student


class StudentTests(unittest.TestCase):
    def setUp(self):
        self.department = Department("SE", "Software Engineering")
        self.course = Course("SE301", "Software Design", 3, 1)
        self.other = Course("SE302", "Database Systems", 4, 30)
        self.student = Student("P1", "Ada", "ada@example.com", "1001", self.department)

    def test_inheritance_and_department_link(self):
        self.assertIsInstance(self.student, Person)
        self.assertEqual(self.student.get_role(), "Student")
        self.assertIn(self.student, self.department.students)

    def test_person_is_abstract(self):
        with self.assertRaises(TypeError):
            Person("P2", "Name", "name@example.com")

    def test_enroll_links_both_sides(self):
        enrollment = self.student.enroll(self.course, "2026-Fall")
        self.assertIn(enrollment, self.student.enrollments)
        self.assertIn(enrollment, self.course.enrollments)

    def test_duplicate_enrollment_rejected(self):
        self.student.enroll(self.other, "2026-Fall")
        with self.assertRaises(ValueError):
            self.student.enroll(self.other, "2026-Fall")

    def test_full_course_leaves_student_unchanged(self):
        self.student.enroll(self.course, "2026-Fall")
        second = Student("P2", "Lin", "lin@example.com", "1002", self.department)
        with self.assertRaises(ValueError):
            second.enroll(self.course, "2026-Fall")
        self.assertEqual(second.enrollments, ())

    def test_drop_removes_both_sides(self):
        self.student.enroll(self.course, "2026-Fall")
        self.student.drop(self.course, "2026-Fall")
        self.assertEqual(self.student.enrollments, ())
        self.assertEqual(self.course.enrollments, ())

    def test_gpa_is_credit_weighted(self):
        self.student.enroll(self.course, "2026-Fall")
        self.student.enroll(self.other, "2026-Fall")
        self.student.assign_grade(self.course, "2026-Fall", "AA")
        self.student.assign_grade(self.other, "2026-Fall", "BB")
        self.assertEqual(self.student.calculate_gpa(), 3.43)

    def test_invalid_grade_rejected(self):
        self.student.enroll(self.course, "2026-Fall")
        with self.assertRaises(ValueError):
            self.student.assign_grade(self.course, "2026-Fall", "XX")


if __name__ == "__main__":
    unittest.main()
