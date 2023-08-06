import ast
import json
import os
import glob

# Get all the text files in r"C:\Users\Harminder Nijjar\Desktop\r6_auto_location\map-data

file_names = glob.glob(r"C:\Users\Harminder Nijjar\Desktop\r6_auto_location\map-data\*.txt")

for file_name in file_names:
    with open(file_name, "r") as file:
        data = file.read()
        try:
            # Replace single quotes with double quotes
            data = data.replace("'", '"')
            # Remove the first part of the JavaScript object (e.g., "bank: {...}") to make it valid JSON.
            json_data = json.loads(data.split(':', 1)[1].strip())
            with open(f"{file_name.split('.')[0]}.json", "w") as json_file:
                json.dump(json_data, json_file, indent=2)
            print(f"Converted {file_name} to {file_name.split('.')[0]}.json")
        except ValueError as e:
            print(f"Error processing {file_name}: {e}")