import os

def to_snake_case(name):
    return name.replace(" ", "_").lower()

current_directory = os.getcwd()

for item in os.listdir(current_directory):
    item_path = os.path.join(current_directory, item)

    if os.path.isdir(item_path):
        new_name = to_snake_case(item)
        new_path = os.path.join(current_directory, new_name)

        if item_path != new_path:
            os.rename(item_path, new_path)
            print(f"Renamed folder: {item} -> {new_name}")

print("All folders have been renamed to snake_case successfully!")
