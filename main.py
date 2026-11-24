from student_system import Course, Department, Instructor, Student

FALL = "2026-2027 Fall"
SPRING = "2026-2027 Spring"

# Credits are model values, not official course data.
CURRENT_COURSES = [
    ("AII003", "Software Engineering"),
    ("AII409", "Object-Oriented Programming II"),
    ("AII415", "Decision Making"),
    ("AII463", "Image Processing"),
    ("COM490", "Engineering Design I"),
    ("ENG202+THM202", "Akademik Yazma Becerileri"),
]


def main() -> None:
    print("AII003 | Software Engineering | Priscilla Olawale\n")
    department = Department("COM", "Computer Engineering")

    # Real student and current courses (no grades yet)
    me = Student("P001", "Gülşah Gümüş", "student@example.com", "20221903", department)
    for code, title in CURRENT_COURSES:
        course = Course(code, title)
        department.add_course(course)
        me.enroll(course, FALL)
    print(me.transcript().render())

    # Sample scenario: fictional student and grades, AII101 -> AII102 prerequisite
    print("\n--- Sample scenario (fictional student and grades) ---\n")
    teacher = Instructor("P100", "Sample Instructor", "instructor@example.com", department)
    sample = Student("P002", "Sample Student", "sample@example.com", "00000000", department)
    aii101 = Course("AII101")
    aii102 = Course("AII102", prerequisites=[aii101])
    for course in (aii101, aii102):
        department.add_course(course)
        teacher.assign_course(course)

    try:
        sample.enroll(aii102, FALL)
    except ValueError as error:
        print(f"Enrollment rejected: {error}\n")

    sample.enroll(aii101, FALL)
    teacher.submit_grade(sample, aii101, FALL, "BA")
    sample.enroll(aii102, SPRING)
    teacher.submit_grade(sample, aii102, SPRING, "AA")
    print(sample.transcript().render())


if __name__ == "__main__":
    main()
