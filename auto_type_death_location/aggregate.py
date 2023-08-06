# Import necessary libraries
import os
import glob
import logging

# Set up logging to capture events when script runs and any possible errors.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('python_files_aggregation.log', mode='a')  # Handles writing log messages to a file.
log_format = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - '
                               '[%(process)d:%(thread)d]')
file_handler.setFormatter(log_format)  # Sets the log message format.
logger.addHandler(file_handler)  # Adds the file handler to the logger.

console_handler = logging.StreamHandler()  # Handles writing log messages to the console.
console_handler.setFormatter(log_format)  # Sets the log message format.
logger.addHandler(console_handler)  # Adds the console handler to the logger.


def read_python_files(directory):
    """
    Reads all Python files in a given directory, excluding the script file itself.
    This helps in gathering the python files that contain modules which we want to feed into ChatGPT.
    """
    # Use glob to find all .py files in the directory.
    python_files = glob.glob(os.path.join(directory, '*.py'))

    # Exclude the script file itself from the files to be processed.
    excluded_file = os.path.join(directory, 'aggregate.py')
    python_files = [file for file in python_files if file != excluded_file]
    
    logger.info("Python files in the directory have been read.")
    return python_files


def read_file_content(file_path):
    """
    Reads the content of a file.
    This allows us to extract the code from each Python file, which we can then pass into ChatGPT.
    """
    with open(file_path, 'r') as file:
        return file.read()


def main():
    """
    Main function to execute the script.
    This function manages the process of reading the Python files, extracting the code, and storing it in a format
    suitable for use with ChatGPT.
    """
    # Get the current working directory.
    current_directory = os.getcwd()

    # Read all Python files in the current directory.
    python_files = read_python_files(current_directory)

    if not python_files:
        logger.error("No Python files found in the current directory.")
        return

    python_code_dict = {}

    # Loop through each Python file and read its content.
    for file_path in python_files:
        file_name = os.path.basename(file_path)
        python_code = read_file_content(file_path)
        python_code_dict[file_name] = python_code
        logger.info(f"File {file_name} has been read.")

    # Save the dictionary to a text file.
    # This format makes it easy to use the collected Python code with ChatGPT.
    output_file = os.path.join(current_directory, 'python_code.txt')
    with open(output_file, 'w') as outfile:
        for file_name, python_code in python_code_dict.items():
            outfile.write(f'"{file_name}" : "{python_code}",\n')

    logger.info(f"Python files have been saved in '{output_file}' with the specified format.")


if __name__ == "__main__":
    main()