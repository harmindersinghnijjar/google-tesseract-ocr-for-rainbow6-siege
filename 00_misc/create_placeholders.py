import os

# Get the current working directory
current_directory = os.getcwd()

# Iterate through all the items in the current directory
for item in os.listdir(current_directory):
    # Construct the full path of the item
    item_path = os.path.join(current_directory, item)

    # Check if the item is a directory
    if os.path.isdir(item_path):
        # Construct the path for the placeholder.txt file within the directory
        placeholder_path = os.path.join(item_path, 'placeholder.txt')

        # Create the placeholder.txt file
        with open(placeholder_path, 'w') as file:
            file.write('This is a placeholder file.')

        print(f"Created placeholder.txt in {item}")

print("All placeholder.txt files have been created successfully!")
