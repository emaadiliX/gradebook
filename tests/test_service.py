"""
Unit tests for gradebook service layer.

Tests cover add_student, add_grade, and compute_average functions.
"""

import unittest
import os
import json
from gradebook import service
from gradebook.storage import load_data, save_data


class TestGradebookService(unittest.TestCase):
    """Test cases for gradebook service functions."""

    def setUp(self):
        """Set up test environment before each test."""
        self.test_data_path = 'data/test_gradebook.json'

        os.makedirs('data', exist_ok=True)

        # Create a clean test data file
        test_data = {
            'students': [],
            'courses': [],
            'enrollments': []
        }
        with open(self.test_data_path, 'w') as f:
            json.dump(test_data, f)

        service.load_data = lambda: load_data(self.test_data_path)
        service.save_data = lambda data: save_data(data, self.test_data_path)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_data_path):
            os.remove(self.test_data_path)

    def test_add_student(self):
        """Test adding a student works correctly."""
        student_id = service.add_student("Arben Krasniqi")

        self.assertEqual(student_id, 1)

        data = load_data(self.test_data_path)
        self.assertEqual(len(data['students']), 1)
        self.assertEqual(data['students'][0]['name'], "Arben Krasniqi")
        self.assertEqual(data['students'][0]['id'], 1)

    def test_add_grade(self):
        """Test adding a grade works correctly."""
        service.add_student("Blerta Hoxha")
        service.add_course("CS101", "Programming 1")
        service.enroll(1, "CS101")

        service.add_grade(1, "CS101", 95.0)

        data = load_data(self.test_data_path)
        enrollment = data['enrollments'][0]
        self.assertEqual(len(enrollment['grades']), 1)
        self.assertEqual(enrollment['grades'][0], 95.0)

    def test_compute_average(self):
        """Test computing average grade works correctly."""
        service.add_student("Dren Osmani")
        service.add_course("MATH201", "Calculus")
        service.enroll(1, "MATH201")
        service.add_grade(1, "MATH201", 80)
        service.add_grade(1, "MATH201", 90)
        service.add_grade(1, "MATH201", 100)

        average = service.compute_average(1, "MATH201")

        self.assertEqual(average, 90.0)

    # Edge case and failure tests

    def test_multiple_students(self):
        """Test that each new student gets a unique ID."""
        id1 = service.add_student("Erza Sejdiu")
        id2 = service.add_student("Flamur Berisha")
        id3 = service.add_student("Gresa Morina")

        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)
        self.assertEqual(id3, 3)

    def test_grade_above_100(self):
        """Test that grade above 100 raises ValueError."""
        service.add_student("Arta Shala")
        service.add_course("ENG102", "English Literature")
        service.enroll(1, "ENG102")

        with self.assertRaises(ValueError) as context:
            service.add_grade(1, "ENG102", 150)

        self.assertIn("between 0 and 100", str(context.exception))

    def test_negative_grade(self):
        """Test that negative grade raises ValueError."""
        service.add_student("Besnik Kelmendi")
        service.add_course("HIST150", "History of Albania")
        service.enroll(1, "HIST150")

        with self.assertRaises(ValueError) as context:
            service.add_grade(1, "HIST150", -10)

        self.assertIn("between 0 and 100", str(context.exception))

    def test_text_grade_raises_error(self):
        """Test that text grade raises TypeError."""
        service.add_student("Diellza Hajdari")
        service.add_course("PHYS101", "Physics")
        service.enroll(1, "PHYS101")

        with self.assertRaises(TypeError) as context:
            service.add_grade(1, "PHYS101", "A+")

        self.assertIn("must be a number", str(context.exception))

    def test_average_with_no_grades(self):
        """Test that average with no grades returns 0.0."""
        service.add_student("Edona Limani")
        service.add_course("ART210", "Digital Art")
        service.enroll(1, "ART210")

        average = service.compute_average(1, "ART210")

        self.assertEqual(average, 0.0)

    def test_average_for_unenrolled_student(self):
        """Test that computing average for unenrolled student raises ValueError."""
        service.add_student("Fisnik Gashi")
        service.add_course("MUS105", "Music Theory")

        with self.assertRaises(ValueError) as context:
            service.compute_average(1, "MUS105")

        self.assertIn("Enrollment not found", str(context.exception))

    def test_grade_for_unenrolled_student(self):
        """Test that adding grade for unenrolled student raises ValueError."""
        service.add_student("Luana Dervishi")
        service.add_course("PE120", "Physical Education")

        with self.assertRaises(ValueError) as context:
            service.add_grade(1, "PE120", 85)

        self.assertIn("Enrollment not found", str(context.exception))


if __name__ == '__main__':
    unittest.main()
