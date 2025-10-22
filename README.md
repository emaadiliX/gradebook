# Gradebook CLI

A command-line application for managing students, courses, enrollments, and grades.

## Setup

### Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Generate Sample Data

```bash
python scripts/seed.py
```

This creates 3 students, 3 courses, and sample grades for testing.

## Usage

### Add Student

```bash
python main.py add-student --name "Rachel Green"
```

### Add Course

```bash
python main.py add-course --code "PHY101" --title "Physics"
```

### Enroll Student

```bash
python main.py enroll --student-id 1 --course CS101
```

### Add Grade

```bash
python main.py add-grade --student-id 1 --course CS101 --grade 95
```

### List Commands

```bash
# List students (sorted by name by default)
python main.py list students
python main.py list students --sort id

# List courses (sorted by code by default)
python main.py list courses
python main.py list courses --sort title

# List enrollments
python main.py list enrollments
```

### Calculate Averages

```bash
# Course average
python main.py avg --student-id 1 --course CS101

# Overall GPA
python main.py gpa --student-id 1
```

## Running Tests

```bash
# Run all tests
python -m unittest tests.test_service

# Run specific test
python -m unittest tests.test_service.TestGradebookService.test_add_student
```

## Design Decisions & Limitations

### Design Decisions

**JSON Storage**: I chose JSON for its simplicity and readability. The data file can be easily inspected and debugged, which is useful during development.

**Three-Layer Architecture**: The code is organized into models, service, and storage layers. This separation makes the codebase easier to maintain and test.

**Auto-Increment IDs**: Students receive sequential IDs automatically (1, 2, 3...). This approach is simple and sufficient for a single-user CLI application.

**GPA Calculation**: The GPA is calculated as the average of all course averages. Credit hours are not considered since they were not part of the requirements.

**Double Validation**: Input validation occurs in both main.py and service.py to ensure data integrity at multiple levels.

**List Comprehensions**: Used throughout service.py for data filtering and transformation (particularly in compute_average and compute_gpa functions), as required by the assignment.

### Limitations

- **No editing or deletion**: Grades cannot be modified or removed once added without manually editing the JSON file
- **Single-user only**: No support for multiple concurrent users or authentication
- **Memory constraints**: All data is loaded into memory, which limits scalability to smaller datasets
- **No weighted GPA**: All courses are treated equally regardless of credit hours
- **Case-sensitive course codes**: "CS101" and "cs101" are treated as different courses
- **No report generation**: Cannot produce formatted transcripts or detailed reports

### Potential Improvements

If this project were to be extended:

- Migrate to SQLite for better performance and scalability
- Implement grade editing and deletion functionality
- Add a web interface for easier access
- Include search and filtering capabilities
- Generate PDF transcripts
- Implement case-insensitive course code matching
- Add data backup and restore features

## Author

Ema Adili
