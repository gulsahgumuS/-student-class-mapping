from student_system import Course, Department, EnrollmentError, Instructor, Student

COURSE_CODE = "AII003"
COURSE_TITLE = "Software Engineering"
INSTRUCTOR_NAME = "Priscilla Olawale"

STUDENT_NAME = "Gülşah Gümüş"
STUDENT_NUMBER = "20221903"

FALL = "2026-2027 Fall"
SPRING = "2026-2027 Spring"

# Credits and capacity are model values, not official course data.
DEFAULT_CREDITS = 3
DEFAULT_CAPACITY = 30

CURRENT_COURSES = [
    (COURSE_CODE, COURSE_TITLE),
    ("AII409", "Object-Oriented Programming II"),
    ("AII415", "Decision Making"),
    ("AII463", "Image Processing"),
    ("COM490", "Engineering Design I"),
    ("ENG202+THM202", "Akademik Yazma Becerileri"),
]


def show_current_courses(department: Department) -> None:
    instructor = Instructor(
        "P100", INSTRUCTOR_NAME, "instructor@example.com", "Instructor", department
    )
    student = Student("P001", STUDENT_NAME, "student@example.com", STUDENT_NUMBER, department)

    for code, title in CURRENT_COURSES:
        course = Course(code, title, DEFAULT_CREDITS, DEFAULT_CAPACITY)
        department.add_course(course)
        if code == COURSE_CODE:
            instructor.assign_course(course)
        student.enroll(course, FALL)

    print(student.transcript().render())


def show_sample_rules(department: Department) -> None:
    """Demonstrates grades and rules with fictional data."""
    print("\n--- Sample scenario (fictional student, courses, and grades) ---\n")

    instructor = Instructor(
        "P200", "Sample Instructor", "sample.instructor@example.com", "Instructor", department
    )
    student = Student("P002", "Sample Student", "sample@example.com", "00000000", department)
    basics = Course("DEMO101", "Sample Basics", 4, DEFAULT_CAPACITY)
    elective = Course("DEMO102", "Sample Elective", 4, DEFAULT_CAPACITY)
    advanced = Course("DEMO201", "Sample Advanced", 4, DEFAULT_CAPACITY, [basics])

    for course in (basics, elective, advanced):
        department.add_course(course)
        instructor.assign_course(course)

    try:
        student.enroll(advanced, FALL)
    except EnrollmentError as error:
        print(f"Enrollment rejected: {error}\n")

    student.enroll(basics, FALL)
    student.enroll(elective, FALL)
    instructor.submit_grade(student, basics, FALL, "BA")
    instructor.submit_grade(student, elective, FALL, "FF")

    student.enroll(advanced, SPRING)
    student.enroll(elective, SPRING)
    instructor.submit_grade(student, advanced, SPRING, "AA")
    instructor.submit_grade(student, elective, SPRING, "BB")

    print(student.transcript().render())


def main() -> None:
    print(f"{COURSE_CODE} | {COURSE_TITLE} | {INSTRUCTOR_NAME}\n")
    department = Department("COM", "Computer Engineering")
    show_current_courses(department)
    show_sample_rules(department)


if __name__ == "__main__":
    main()
