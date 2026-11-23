# Mapping Design to Code: Student Class Diagram

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
        +get_role() str
        +enroll(course, semester) Enrollment
        +drop(course, semester) void
        +assign_grade(course, semester, grade) void
        +calculate_gpa() float
    }
    class Department {
        +code: str
        +name: str
        +add_student(student) void
        +add_course(course) void
    }
    class Course {
        +code: str
        +title: str
        +credits: int
        +capacity: int
        +is_full() bool
        +add_enrollment(enrollment) void
        +remove_enrollment(enrollment) void
    }
    class Enrollment {
        +semester: str
        +enrolled_on: date
        -grade: str
        +assign_grade(grade) void
        +grade_points() float
    }

    Person <|-- Student
    Department "1" o-- "0..*" Student
    Department "1" o-- "0..*" Course
    Student "1" --> "0..*" Enrollment
    Course "1" --> "0..*" Enrollment
```

## Design-to-Code Mapping

| UML element | Code |
| --- | --- |
| Class | Python `class`, one module per class |
| Abstract class `Person` | `ABC` with an `@abstractmethod` |
| Private attribute (`-`) | `_attribute` with a read-only `@property` |
| Public attribute (`+`) | Instance attribute |
| Operation | Method |
| Inheritance `Student` to `Person` | `class Student(Person)` and `super().__init__()` |
| Aggregation with `Department` | `Department` keeps lists of existing objects |
| Association class `Enrollment` | Holds `student`, `course`, semester, and grade |
| Multiplicity `0..*` | `list` |
| Multiplicity `1` | Required constructor argument |

## Run

Requires Python 3.9 or newer. No external packages are needed.

```bash
python main.py
python -m unittest discover tests
```
