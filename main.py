import argparse
import sys
import os
import gradebook.service as service
import logging

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def validate_student_name(name):
    if not name or name.strip() == "":
        raise ValueError("Student name cannot be empty")
    return name.strip()


def validate_course_code(code):
    if not code or code.strip() == "":
        raise ValueError("Course code cannot be empty")
    code = code.strip()
    if len(code) < 2:
        raise ValueError("Course code must be at least 2 characters long")
    return code


def validate_course_title(title):
    if not title or title.strip() == "":
        raise ValueError("Course title cannot be empty")
    return title.strip()


def parse_grade(grade):
    try:
        grade_value = float(grade)
    except ValueError:
        raise ValueError("Grade must be a number")

    if grade_value < 0 or grade_value > 100:
        raise ValueError("Grade must be between 0 and 100")

    return grade_value


def validate_student_id(student_id):
    try:
        id_value = int(student_id)
    except ValueError:
        raise ValueError("Student ID must be a number")

    if id_value <= 0:
        raise ValueError("Student ID must be positive")

    return id_value


def main():
    parser = argparse.ArgumentParser(description='Gradebook CLI')
    subparsers = parser.add_subparsers(dest='command')

    # add-student command
    add_student_parser = subparsers.add_parser('add-student')
    add_student_parser.add_argument('--name', required=True)

    # add-course command
    add_course_parser = subparsers.add_parser('add-course')
    add_course_parser.add_argument('--code', required=True)
    add_course_parser.add_argument('--title', required=True)

    # enroll command
    enroll_parser = subparsers.add_parser('enroll')
    enroll_parser.add_argument('--student-id', required=True)
    enroll_parser.add_argument('--course', required=True)

    # add-grade command
    grade_parser = subparsers.add_parser('add-grade')
    grade_parser.add_argument('--student-id', required=True)
    grade_parser.add_argument('--course', required=True)
    grade_parser.add_argument('--grade', required=True)

    # list command
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument(
        'type', choices=['students', 'courses', 'enrollments'])
    list_parser.add_argument('--sort', choices=['name', 'code'])

    # avg command
    avg_parser = subparsers.add_parser('avg')
    avg_parser.add_argument('--student-id', required=True)
    avg_parser.add_argument('--course', required=True)

    # gpa command
    gpa_parser = subparsers.add_parser('gpa')
    gpa_parser.add_argument('--student-id', required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'add-student':
            validated_name = validate_student_name(args.name)
            logging.info("Adding student: " + validated_name)
            service.add_student(validated_name)

        elif args.command == 'add-course':
            validated_code = validate_course_code(args.code)
            validated_title = validate_course_title(args.title)
            logging.info("Adding course: " + validated_code +
                         " - " + validated_title)
            service.add_course(validated_code, validated_title)

        elif args.command == 'enroll':
            validated_student_id = validate_student_id(args.student_id)
            validated_course_code = validate_course_code(args.course)
            logging.info("Enrolling student " + str(validated_student_id) +
                         " in course " + validated_course_code)
            service.enroll(validated_student_id, validated_course_code)

        elif args.command == 'add-grade':
            validated_student_id = validate_student_id(args.student_id)
            validated_grade = parse_grade(args.grade)
            logging.info("Adding grade " + str(validated_grade) + " for student " +
                         str(validated_student_id) + " in course " + args.course)
            service.add_grade(validated_student_id,
                              args.course, validated_grade)

        elif args.command == 'list':
            logging.info("Listing " + args.type)
            if args.type == 'students':
                students = service.list_students()
                if len(students) == 0:
                    print("No students found.")
                else:
                    print("Students:")
                    for s in students:
                        print("ID: " + str(s['id']) + ", Name: " + s['name'])

            elif args.type == 'courses':
                courses = service.list_courses()
                if len(courses) == 0:
                    print("No courses found.")
                else:
                    print("Courses:")
                    for c in courses:
                        print("Code: " + c['code'] + ", Title: " + c['title'])

            elif args.type == 'enrollments':
                enrollments = service.list_enrollments()
                if len(enrollments) == 0:
                    print("No enrollments found.")
                else:
                    print("Enrollments:")
                    for e in enrollments:
                        if len(e['grades']) > 0:
                            grades_display = ""
                            for grade in e['grades']:
                                grades_display = grades_display + \
                                    str(grade) + ", "
                            grades_display = grades_display[:-2]
                        else:
                            grades_display = "No grades yet"

                        print("Student ID: " + str(e['student_id']) +
                              ", Course: " + e['course_code'] +
                              ", Grades: [" + grades_display + "]")

        elif args.command == 'avg':
            validated_student_id = validate_student_id(args.student_id)
            logging.info("Computing average for student " +
                         str(validated_student_id) + " in course " + args.course)
            average = service.compute_average(
                validated_student_id, args.course)
            print("Average grade for student " + str(validated_student_id) +
                  " in " + args.course + ": " + str(round(average, 2)))

        elif args.command == 'gpa':
            validated_student_id = validate_student_id(args.student_id)
            logging.info("Computing GPA for student " +
                         str(validated_student_id))
            gpa = service.compute_gpa(validated_student_id)
            print("GPA for student " + str(validated_student_id) +
                  ": " + str(round(gpa, 2)))

    except ValueError as e:
        logging.error("ValueError occurred: " + str(e))
        print("Error: " + str(e))
        sys.exit(1)
    except TypeError as e:
        print("Error: " + str(e))
        sys.exit(1)
    except Exception as e:
        logging.error("Unexpected error occurred: " + str(e))
        print("An error occurred: " + str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
