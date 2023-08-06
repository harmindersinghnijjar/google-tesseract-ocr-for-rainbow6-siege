"""Select an OCR Engine: You may choose an existing OCR engine like Tesseract or create a custom neural network-based OCR.

Gather Training Data: Collect a set of images with known text and the corresponding labels.

Preprocess the Data: Apply techniques such as resizing, thresholding, noise reduction, etc., to make the text extraction more accurate.

Train the OCR Engine: Use the processed images to train the OCR engine. You may employ supervised learning, where you provide both input images and correct output labels.

Create a Feedback Loop: Implement a user interface or another mechanism to allow human users to correct OCR mistakes. This corrected data can then be added back into the training set.

Retrain Periodically: Use the newly corrected data to retrain the OCR engine periodically, thus enabling continuous improvement.

Evaluate and Monitor Performance: Set up metrics to evaluate the OCR engine's performance, and monitor them over time to understand how the engine is improving with the new feedback data."""

from difflib import get_close_matches
import json
import os
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


# Function to handle mouse clicks
def on_click(event):
    # Get the coordinates of the click
    x, y = event.x, event.y
    # Process the coordinates (you can add your logic here)
    # For example: death_coordinates.append((x, y))

def on_release(event):
    # Perform any actions needed on mouse release (if required)
    pass

# Load the coordinates
with open('feed_coordinates.txt', 'r') as f:
    death_coordinates = json.loads(f.read())

with open('location_coordinates.txt', 'r') as f:
    location_coordinates = json.loads(f.read())

# Function to perform OCR on a specific region of the screen
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

# Function to type a string using keyboard.press_and_release()
def type_string(string):
    keyboard.write(string, delay=0.001)

# Main loop
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
        know_locations = []
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



    # Wait for 0.5 seconds to avoid overwhelming the system
    time.sleep(0.5)
