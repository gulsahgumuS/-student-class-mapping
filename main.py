from student_system import Course, Department, Student


def main() -> None:
    department = Department("SE", "Software Engineering")
    design = Course("SE301", "Software Design", 3, 30)
    databases = Course("SE302", "Database Systems", 4, 30)
    department.add_course(design)
    department.add_course(databases)

    student = Student("P001", "Sample Student", "student@example.com", "20260001", department)
    student.enroll(design, "2026-Fall")
    student.enroll(databases, "2026-Fall")
    student.assign_grade(design, "2026-Fall", "AA")
    student.assign_grade(databases, "2026-Fall", "BB")

    print(f"{student.name} ({student.get_role()}) - {department.name}")
    for enrollment in student.enrollments:
        print(f"{enrollment.course.code} {enrollment.course.title}: {enrollment.grade}")
    print(f"GPA: {student.calculate_gpa()}")


if __name__ == "__main__":
    main()
