"""
Storage layer for gradebook data persistence.

Handles loading and saving gradebook data to/from JSON files.
"""

import json
import os
import logging


def load_data(path='data/gradebook.json'):
    """
    Load gradebook data from a JSON file.

    Args: path: Path to the JSON file (default: 'data/gradebook.json')

    Returns:
        Dictionary containing students, courses, and enrollments lists.
        Returns empty structure if file doesn't exist.

    Logs loading attempts and results to logs/app.log
    """

    logging.info("Attempting to load data from " + path)

    if not os.path.exists(path):
        logging.info("File does not exist, returning empty data")
        return {'students': [], 'courses': [], 'enrollments': []}

    try:
        with open(path, "r") as f:
            data = json.load(f)
        logging.info("Successfully loaded data from " + path)
        return data

    except json.JSONDecodeError:
        logging.error("Could not read JSON in '" +
                      path + "', file might be corrupted")
        print(f"Could not read JSON in '{path}', file might be corrupted.")
        return {'students': [], 'courses': [], 'enrollments': []}


def save_data(data, path='data/gradebook.json'):
    """
    Save gradebook data to a JSON file.

    Args:
        data: Dictionary containing students, courses, and enrollments
        path: Path to the JSON file (default: 'data/gradebook.json')

    Creates parent directories if they don't exist.
    Logs save attempts and results to logs/app.log
    """
    logging.info("Attempting to save data to " + path)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logging.info("Data successfully saved to " + path)
        print(f"Data successfully saved to '{path}'.")
    except OSError as e:
        logging.error("Error saving data to '" + path + "': " + str(e))
        print(f"Error saving data to '{path}': {e}")
