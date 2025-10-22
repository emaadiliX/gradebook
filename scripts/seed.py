"""
Seed script to populate gradebook with sample data.

Creates students, courses, enrollments, and grades for testing purposes.
"""
import sys
import os
import json

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import gradebook.service as service

def clear_data():
    """Clear existing gradebook data."""
    data_path = 'data/gradebook.json'
    
    os.makedirs('data', exist_ok=True)
    
    empty_data = {
        'students': [],
        'courses': [],
        'enrollments': []
    }
    
    with open(data_path, 'w') as f:
        json.dump(empty_data, f, indent=2)
    
    print("Cleared existing data.")

def seed_data():
    """Populate the gradebook with sample data."""
    print("Starting to populate gradebook with data...")

    # Add students
    print("\nAdding students...")
    student1_id = service.add_student("Ema Adili")
    student2_id = service.add_student("Rina Uka")
    student3_id = service.add_student("Rona Berisha")

    # Add courses
    print("\nAdding courses...")
    service.add_course("CS101", "Introduction to Computer Science")
    service.add_course("ENG102", "English Literature")
    service.add_course("MATH201", "Advanced Mathematics")

    # Enroll students in courses
    print("\nEnrolling students...")
    service.enroll(student1_id, "CS101")
    service.enroll(student1_id, "ENG102")

    service.enroll(student2_id, "CS101")
    service.enroll(student2_id, "MATH201")

    service.enroll(student3_id, "CS101")
    service.enroll(student3_id, "ENG102")

    print("\nAdding grades...")

    # Ema's grades
    service.add_grade(student1_id, "CS101", 95)
    service.add_grade(student1_id, "CS101", 88)
    service.add_grade(student1_id, "CS101", 90)

    service.add_grade(student1_id, "ENG102", 82)
    service.add_grade(student1_id, "ENG102", 86)

    # Rina's grades
    service.add_grade(student2_id, "CS101", 75)
    service.add_grade(student2_id, "CS101", 80)
    service.add_grade(student2_id, "CS101", 70)

    service.add_grade(student2_id, "MATH201", 90)
    service.add_grade(student2_id, "MATH201", 92)

    # Rona's grades
    service.add_grade(student3_id, "CS101", 100)
    service.add_grade(student3_id, "CS101", 97)

    service.add_grade(student3_id, "ENG102", 85)
    service.add_grade(student3_id, "ENG102", 88)
    service.add_grade(student3_id, "ENG102", 91)

    print("\n" + "-" * 50)
    print("Seeding complete!")
    print("\nSummary:")
    print("- 3 students added")
    print("- 3 courses added")
    print("- 6 enrollments created")
    print("- 15 grades recorded")
    print("\nData saved to data/gradebook.json")


if __name__ == '__main__':
    seed_data()
