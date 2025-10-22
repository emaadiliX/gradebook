"""
Service layer for gradebook operations.
Contains business logic for managing students, courses, enrollments, and grades.
"""

from gradebook.models import Student, Course, Enrollment
from .storage import load_data, save_data


def add_student(name):
    """
    Add a new student to the gradebook.

    Args: name: Student name as a string

    Returns: The new student ID
    """
    data = load_data()

    if data["students"]:
        new_id = max(s["id"] for s in data["students"]) + 1
    else:
        new_id = 1

    data["students"].append({"id": new_id, "name": name.strip()})

    save_data(data)

    print(f"Student '{name}' added with ID {new_id}.")
    return new_id


def add_course(code, title):
    """
    Add a new course to the gradebook.

    Args:
        code: Course code (e.g., 'CS101')
        title: Course title

    Returns: The new Course object

    Raises a ValueError if course code already exists
    """
    data = load_data()

    for course in data['courses']:
        if course['code'] == code:
            raise ValueError(f"Course with code {code} already exists")

    new_course = Course(code, title)

    data['courses'].append({
        'code': new_course.code,
        'title': new_course.title
    })

    save_data(data)
    print(
        f"Course '{new_course.title}' - {new_course.code} added successfully.")
    return new_course


def enroll(student_id, course_code):
    """
    Enroll a student in a course.

    Args:
        student_id: Student ID number
        course_code: Course code (e.g., 'CS101')

    Returns: The new Enrollment object, or None if enrollment failed
    """
    data = load_data()

    if not any(s["id"] == student_id for s in data["students"]):
        print(f"No student found with ID {student_id}.")
        return
    if not any(c["code"] == course_code for c in data["courses"]):
        print(f"No course found with code '{course_code}'.")
        return

    if any(e["student_id"] == student_id and e["course_code"] == course_code for e in data["enrollments"]):
        print(f"Student {student_id} is already enrolled in {course_code}.")
        return

    new_enrollment = Enrollment(student_id, course_code, [])

    data['enrollments'].append({
        'student_id': new_enrollment.student_id,
        'course_code': new_enrollment.course_code,
        'grades': new_enrollment.grades
    })

    save_data(data)
    print(
        f"Student '{new_enrollment.student_id}' enrolled into {new_enrollment.course_code} successfully.")
    return new_enrollment


def add_grade(student_id, course_code, grade):
    """
    Add a grade for a student in a course.

    Args:
        student_id: Student ID number
        course_code: Course code
        grade: Grade value (0-100)

    Raises:
        TypeError: If grade is not a number
        ValueError: If grade is not between 0 and 100
        ValueError: If enrollment not found
    """

    data = load_data()

    if not isinstance(grade, (int, float)):
        raise TypeError("Grade must be a number.")
    if not (0 <= grade <= 100):
        raise ValueError("Grade must be between 0 and 100.")

    for enrollment in data['enrollments']:
        if enrollment['student_id'] == student_id and enrollment['course_code'] == course_code:
            enrollment['grades'].append(grade)
            save_data(data)
            return

    raise ValueError(
        f"Enrollment not found for student {student_id} in course {course_code}")


def list_students():
    """
    Get a sorted list of all students.
    """
    data = load_data()
    return sorted(data["students"], key=lambda s: s["name"].lower())


def list_courses():
    """
    Get a sorted list of all courses.
    """
    data = load_data()
    return sorted(data["courses"], key=lambda c: c["code"].lower())


def list_enrollments():
    """
    Get a sorted list of all enrollments.
    """
    data = load_data()
    return sorted(data["enrollments"], key=lambda e: (e["student_id"], e["course_code"]))


def compute_average(student_id, course_code):
    """
    Compute the average grade for a student in a course.

    Args:
        student_id: Student ID number
        course_code: Course code

    Returns:
        Average grade as a float, or 0.0 if no grades

    Raises:
        ValueError: If enrollment not found
    """
    data = load_data()

    for enrollment in data['enrollments']:
        if enrollment['student_id'] == student_id and enrollment['course_code'] == course_code:
            grades = enrollment['grades']
            if not grades:
                return 0.0
            return sum(grades) / len(grades)

    raise ValueError(
        f"Enrollment not found for student {student_id} in course {course_code}")


def compute_gpa(student_id):
    """
    Compute the GPA for a student across all courses.

    GPA is calculated as the average of all course averages.

    Args:
        student_id: Student ID number

    Returns:
        GPA as a float, or 0.0 if no grades

    Raises:
        ValueError: If student not found
    """
    data = load_data()

    student_exists = any(s['id'] == student_id for s in data['students'])
    if not student_exists:
        raise ValueError(f"Student {student_id} not found")

    student_enrollments = [e for e in data['enrollments']
                           if e['student_id'] == student_id]

    if not student_enrollments:
        return 0.0

    course_averages = []
    for enrollment in student_enrollments:
        grades = enrollment['grades']
        if grades:
            course_averages.append(sum(grades) / len(grades))

    if not course_averages:
        return 0.0

    return sum(course_averages) / len(course_averages)
