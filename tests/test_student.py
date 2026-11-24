import unittest

from student_system import Course, Department, EnrollmentStatus, Instructor, Person, Student

FALL = "2026-2027 Fall"
SPRING = "2026-2027 Spring"


class StudentSystemTests(unittest.TestCase):
    def setUp(self):
        self.department = Department("COM", "Computer Engineering")
        self.course = Course("AII101", capacity=1)
        self.other = Course("AII201", credits=4)
        self.student = Student("P1", "Ada", "ada@example.com", "1001", self.department)
        self.teacher = Instructor("P9", "Grace", "grace@example.com", self.department)

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
        with self.assertRaises(ValueError):
            self.student.enroll(self.other, FALL)

    def test_full_course_is_per_semester(self):
        self.student.enroll(self.course, FALL)
        second = Student("P2", "Lin", "lin@example.com", "1002", self.department)
        with self.assertRaises(ValueError):
            second.enroll(self.course, FALL)
        self.assertEqual(second.enrollments, [])
        second.enroll(self.course, SPRING)

    def test_drop_rules(self):
        self.student.enroll(self.course, FALL)
        self.student.drop(self.course, FALL)
        self.assertEqual(self.course.enrollments, [])
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "BB")
        with self.assertRaises(ValueError):
            self.student.drop(self.other, FALL)

    def test_prerequisite_required(self):
        advanced = Course("AII102", prerequisites=[self.other])
        with self.assertRaises(ValueError):
            self.student.enroll(advanced, FALL)
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "CC")
        self.student.enroll(advanced, SPRING)

    def test_credit_limit(self):
        self.student.enroll(Course("BIG", credits=28), FALL)
        with self.assertRaises(ValueError):
            self.student.enroll(self.course, FALL)

    def test_gpa_is_credit_weighted(self):
        self.assertIsNone(self.student.calculate_gpa())
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
        with self.assertRaises(ValueError):
            self.student.enroll(self.other, "2027-2028 Fall")

    def test_invalid_grade_rejected(self):
        self.student.enroll(self.course, FALL)
        with self.assertRaises(ValueError):
            self.student.assign_grade(self.course, FALL, "XX")

    def test_only_course_instructor_can_grade(self):
        self.student.enroll(self.other, FALL)
        with self.assertRaises(ValueError):
            self.teacher.submit_grade(self.student, self.other, FALL, "AA")
        self.teacher.assign_course(self.other)
        self.teacher.submit_grade(self.student, self.other, FALL, "AA")
        self.assertEqual(self.student.calculate_gpa(), 4.0)

    def test_transcript(self):
        self.student.enroll(self.other, FALL)
        self.student.assign_grade(self.other, FALL, "BA")
        report = self.student.transcript().render()
        self.assertIn("AII201", report)
        self.assertIn("Cumulative GPA: 3.50", report)


if __name__ == "__main__":
    unittest.main()
