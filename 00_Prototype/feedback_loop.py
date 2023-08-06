from difflib import get_close_matches
import json
import os
import re
import time
import random
import tkinter
import editdistance
import pytesseract
import pyautogui
import keyboard
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import tkinter as tk

# Set the path to the Tesseract executable
# You need to adjust this path depending on your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_function(screenshot_path):
    location_text = ocr_region(location_coordinates, save_screenshot=True, screenshot_path="location_screenshot.png")
    return location_text

def save_incorrect_ocr(screenshot_path, incorrect_reading, correct_reading):
    # A dictionary to hold the incorrect reading and the correct reading.
    incorrect_ocr_dict = {
        "screenshot_path": screenshot_path,
        "incorrect_reading": incorrect_reading,
        "correct_reading": correct_reading
    }
    # The path to the file where you'll save the incorrect readings.
    incorrect_ocr_file = 'incorrect_ocr.json'
    
    # Check if the file already exists.
    if os.path.exists(incorrect_ocr_file):
        # If the file exists, load the existing data.
        with open(incorrect_ocr_file, 'r') as file:
            data = json.load(file)
    else:
        # If the file doesn't exist, create an empty list to hold the data.
        data = []

    # Add the new incorrect reading to the data.
    data.append(incorrect_ocr_dict)

    # Save the updated data back to the file.
    with open(incorrect_ocr_file, 'w') as file:
        json.dump(data, file)

# Function to get the most similar location taking into account the previous 5 locations
def compare_locations(location_list, known_locations):
    similarity_scores = {}
    for location in location_list:
        lowest_score = float('inf')
        best_match = None
        for known_location in known_locations:
            score = editdistance.eval(location, known_location)
            if score < lowest_score:
                lowest_score = score
                best_match = known_location
        similarity_scores[location] = (best_match, lowest_score)
    most_similar_location = min(similarity_scores, key=similarity_scores.get)

    return most_similar_location

def on_click(event):
    # ...
    pass

def on_release(event):
    # ...
    pass



with open('feed_coordinates.txt', 'r') as f:
    death_coordinates = json.loads(f.read())

with open('location_coordinates.txt', 'r') as f:
    location_coordinates = json.loads(f.read())

def ocr_region(coordinates, save_screenshot=False, screenshot_path=None):
    x1, y1 = coordinates[0]
    x2, y2 = coordinates[1]
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    # Convert the screenshot to grayscale
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    blur = cv2.GaussianBlur(image, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    # Save the processed image
    if save_screenshot and screenshot_path is not None:
        screenshot.save(screenshot_path)

    # Enlarge the image to improve OCR accuracy
    screenshot = screenshot.resize((screenshot.width * 2, screenshot.height * 2))

    try:
        text = pytesseract.image_to_string(screenshot)
    except pytesseract.TesseractError as e:
        print(f"Error during OCR: {e}")
        text = ""

    # Ignore ♀ character (Unicode code point U+2640)
    text = text.replace('♀', '')
    # Replace any non-alphanumeric characters with a space
    text = ''.join([c if c.isalnum() else ' ' for c in text])
    # Remove any leading or trailing spaces
    text = text.strip()
    # Remove any consecutive spaces
    text = ' '.join(text.split())


    return text

def type_string(string):
    keyboard.write(string, delay=0.001)

def is_ocr_correct(text):
    correct = input("Is the OCR correct? (y/n)")
    if correct == "y":
        return True
    elif correct == "n":
        return False
    else:
        print("Invalid input")
        return is_ocr_correct(text)

while True:
    # Perform OCR on the 'location' region
    location_text = ocr_region(location_coordinates, save_screenshot=True, screenshot_path="location_screenshot.png")

    # Perform OCR on the 'death' region
    death_text = ocr_region(death_coordinates)

    # If the specific text is detected, type out the location
    if "SpaceAgeGames" in death_text:
        print("Death detected")
        print("Opening team chat")
        keyboard.press_and_release('y')
        time.sleep(0.5)
        # Type out the location
        print("Typing location")
        type_string(location_text)
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        time.sleep(5)

    else:
        print(f"Death not detected, current location: {location_text}")
        known_locations = []
        with open("known_locations.txt", "r") as f:
            known_locations = [line.strip() for line in f.readlines()]
        # Use a fuzzy matching algorithm to find the most similar location taking into account the previous 5 locations
        most_similar_location = compare_locations([location_text], known_locations)
        print(f"Most similar location: {most_similar_location}")
        # If the most similar location is not the same as the current location, type out the location
        if most_similar_location != location_text:
            print("Opening team chat")
            keyboard.press_and_release('y')
            time.sleep(0.5)
            # Type out the location
            print("Typing location")
            type_string(most_similar_location)
            time.sleep(0.5)
            keyboard.press_and_release('enter')
            time.sleep(5)

    

    # Check if the OCR reading is correct.
    if not is_ocr_correct(location_text):
        # If the OCR reading is incorrect, save the screenshot and the incorrect reading.
        save_incorrect_ocr("location_screenshot.png", location_text, most_similar_location)
        # Open the screenshot in the default image viewer.
        os.startfile("location_screenshot.png")
        # Wait for the user to close the image viewer.
        input("Press enter when you're done")
        # Delete the screenshot.
        os.remove("location_screenshot.png")

    # Wait for 5 seconds before performing OCR again.
    time.sleep(5)
