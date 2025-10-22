import json
import os
import logging

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_data(path='data/gradebook.json'):

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
        logging.error("Could not read JSON in '" + path + "', file might be corrupted")
        print(f"Could not read JSON in '{path}', file might be corrupted.")


def save_data(data, path='data/gradebook.json'):
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
