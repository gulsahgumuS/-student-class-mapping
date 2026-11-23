# Mapping Design to Code: Student Class Diagram

**Course:** AII003 | Software Engineering | Priscilla Olawale

**Student:** Gülşah Gümüş | 20221903

This project maps a UML class diagram of a student system to Python code.

## Class Diagram

```mermaid
classDiagram
    class Person {
        <<abstract>>
        -person_id: str
        -name: str
        -email: str
        +get_role()* str
    }
    class Student {
        +student_number: str
        +MAX_SEMESTER_CREDITS: int
        +enroll(course, semester) Enrollment
        +drop(course, semester) void
        +assign_grade(course, semester, grade) void
        +calculate_gpa(semester) float
        +earned_credits() int
        +transcript() Transcript
    }
    class Instructor {
        +title: str
        +assign_course(course) void
        +submit_grade(student, course, semester, grade) void
    }
    class Department {
        +code: str
        +name: str
        +add_student(student) void
        +add_instructor(instructor) void
        +add_course(course) void
    }
    class Course {
        +code: str
        +title: str
        +credits: int
        +capacity: int
        +is_full(semester) bool
    }
    class Enrollment {
        +semester: str
        +enrolled_on: date
        -grade: Grade
        +status: EnrollmentStatus
        +assign_grade(grade) void
        +grade_points() float
    }
    class Grade {
        <<enumeration>>
        AA BA BB CB CC DC DD FF
    }
    class EnrollmentStatus {
        <<enumeration>>
        ACTIVE PASSED FAILED
    }
    class Transcript {
        +render() str
    }

    Person <|-- Student
    Person <|-- Instructor
    Department "1" o-- "0..*" Student
    Department "1" o-- "0..*" Instructor
    Department "1" o-- "0..*" Course
    Instructor "0..1" --> "0..*" Course : teaches
    Course "0..*" --> "0..*" Course : prerequisites
    Student "1" --> "0..*" Enrollment
    Course "1" --> "0..*" Enrollment
    Enrollment --> Grade
    Enrollment --> EnrollmentStatus
    Student ..> Transcript : creates
```

## Design-to-Code Mapping

| UML element | Code |
| --- | --- |
| Class | Python `class`, one module per main class |
| Abstract class `Person` | `ABC` with an `@abstractmethod` |
| Private attribute (`-`) | `_attribute` with a read-only `@property` |
| Public attribute (`+`) | Instance attribute |
| Operation | Method |
| Inheritance | `class Student(Person)`, `class Instructor(Person)` |
| Polymorphism | Each subclass implements `get_role()` |
| Aggregation with `Department` | `Department` keeps lists of existing objects |
| Association class `Enrollment` | Holds student, course, semester, and grade |
| Self-association | `Course.prerequisites` |
| Enumeration | `Grade` and `EnrollmentStatus` use `Enum` |
| Dependency | `Student.transcript()` creates a `Transcript` |
| Multiplicity `0..*` | `list` or `tuple` |
| Multiplicity `1` | Required constructor argument |

## Business Rules

- A student cannot enroll twice in the same course in one semester.
- Course capacity is checked per semester.
- Prerequisites must be passed before enrollment.
- A student can take at most 30 credits per semester.
- A failed course can be retaken, and only the latest grade counts in the GPA.
- A passed course cannot be retaken, and a graded course cannot be dropped.
- Only the course instructor can submit a grade.

## Run

Requires Python 3.9 or newer. No external packages are needed.

The program lists the 2026-2027 Fall courses without grades. Grades and rules are
demonstrated in a separate scenario with fictional data. Credits and capacities are
model values, not official course data.

```bash
python main.py
python -m unittest discover tests
```
