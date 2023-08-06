import os
import re
import logging

# Set up logging to capture events when script runs and any possible errors.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

script_name = os.path.basename(__file__).split('.')[0]  # Get the name of the current script
file_handler = logging.FileHandler(f'{script_name}.log', mode='a')  # Handles writing log messages to a file.
log_format = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - '
                               '[%(process)d:%(thread)d]')
file_handler.setFormatter(log_format)  # Sets the log message format.
logger.addHandler(file_handler)  # Adds the file handler to the logger.

console_handler = logging.StreamHandler()  # Handles writing log messages to the console.
console_handler.setFormatter(log_format)  # Sets the log message format.
logger.addHandler(console_handler)  # Adds the console handler to the logger.

# Define the pattern
pattern = re.compile(r'^floor_[1-4fb]f_location_.*$')

# Define the directory path (update accordingly)
directory_path = os.getcwd()

try:
    # Read the file and check each line
    with open(os.path.join(directory_path, 'yolo_r6_location_labels.txt'), 'r') as file:
        incorrect_lines = []
        for line in file:
            line = line.strip()  # Remove any leading/trailing whitespace
            if not pattern.match(line):
                logger.warning(f"Line does not match pattern: {line}")
                # Get the line number and contents
                line_number = sum(1 for _ in file)  # Get the line number
                line_contents = line  # Get the line contents
                incorrect_lines.append((line_number, line_contents))
                logger.warning(f"Line {line_number}: {line_contents}")
            else:
                logger.info(f"Line matches pattern: {line}")
    logger.info("File validation completed successfully!")
    logger.warning(f"Lines that do not match the pattern: {incorrect_lines}")

except FileNotFoundError:
    logger.error(f"File yolo_r6_location_labels.txt not found in directory {directory_path}.")
except Exception as e:
    logger.error(f"An unexpected error occurred: {str(e)}")

