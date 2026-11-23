"""Domain errors. All inherit from ValueError so callers can catch them together."""


class EnrollmentError(ValueError):
    """Base class for enrollment rule violations."""


class DuplicateEnrollmentError(EnrollmentError):
    pass


class CourseFullError(EnrollmentError):
    pass


class PrerequisiteError(EnrollmentError):
    pass


class CreditLimitError(EnrollmentError):
    pass


class InvalidGradeError(ValueError):
    pass


class NotCourseInstructorError(ValueError):
    pass
