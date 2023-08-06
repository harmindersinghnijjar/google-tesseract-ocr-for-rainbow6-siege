import json
import screenshot

if __name__ == "__main__":
    with open("known_locations.txt", "r") as f:
        known_locations = [line.strip() for line in f.readlines()]

    screenshot.save_location()

    with open('location_list.txt', 'r') as f:
        location_list = json.loads(f.read())
    most_similar_location = screenshot.compare_locations(location_list, known_locations)
    print(most_similar_location)
