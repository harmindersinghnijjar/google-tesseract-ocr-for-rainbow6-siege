import os
import re

# Define the pattern
pattern = re.compile(r'^floor_[1-4fb]f_location_.*$')

# Define the directory path (update accordingly)
directory_path = os.getcwd()

# Read the file and check each line
with open(os.path.join(directory_path, 'yolo_r6_location_labels.txt'), 'r') as file:
    for line in file:
        line = line.strip() # Remove any leading/trailing whitespace
        if not pattern.match(line):
            print(f"Line does not match pattern: {line}")
            # You can take additional actions here if needed
