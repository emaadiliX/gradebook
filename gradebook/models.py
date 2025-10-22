"""
Data models for the gradebook application.

Contains Student, Course, and Enrollment classes with validation.
"""


class Student:
    """
    Represents a student in the gradebook.
    """

    def __init__(self, id, name):
        """
        Create a new Student.

        Args:
            id: Student ID (must not be empty)
            name: Student name (must be non-empty string)

        Raises a ValueError if id is empty or name is invalid
        """
        if not id:
            raise ValueError("Students must have an id.")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Please provide a valid name.")

        self.id = id
        self.name = name.strip()

    def __str__(self):
        """Return string representation of the student."""
        return f"Student {self.name} - id {self.id}."


class Course:
    def __init__(self, code, title):
        if not isinstance(code, str) or code.strip() == "":
            raise ValueError("Please provide a valid course code like 'CS101'")
        if not isinstance(title, str) or title.strip() == "":
            raise ValueError("Please provide a valid title.")

        self.code = code
        self.title = title

    def __str__(self):
        return f"Course {self.title} - code {self.code}."


class Enrollment:
    def __init__(self, student_id, course_code, grades: list):
        if not student_id:
            raise ValueError("student_id cannot be empty")
        if not isinstance(course_code, str) or course_code.strip() == "":
            raise ValueError("Please provide a valid course code like 'CS101'")

        if not isinstance(grades, list):
            raise TypeError(
                "Grades must be provided as a list, e.g., [80, 90, 100].")

        for grade in grades:
            if not isinstance(grade, (int, float)):
                raise TypeError("Each grade must be a number.")
            if grade < 0 or grade > 100:
                raise ValueError("Each grade must be between 0 and 100.")

        self.student_id = student_id
        self.course_code = course_code
        self.grades = grades

    def __str__(self):
        return f"Student with id {self.student_id} has enrolled in course with code {self.course_code} and has a grade of {self.grades}."
