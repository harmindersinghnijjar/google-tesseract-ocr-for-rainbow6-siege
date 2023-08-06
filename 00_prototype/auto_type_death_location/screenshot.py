import json
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
import editdistance
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_region(coordinates, save_screenshot=False, screenshot_path=None):
    x1, y1 = coordinates[0]
    x2, y2 = coordinates[1]
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(image, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    if save_screenshot and screenshot_path is not None:
        cv2.imwrite(screenshot_path, opening)
    img_pil = Image.fromarray(opening)
    img_pil = img_pil.resize((img_pil.width * 2, img_pil.height * 2))
    try:
        text = pytesseract.image_to_string(img_pil)
    except pytesseract.TesseractError as e:
        print(f"Error during OCR: {e}")
        text = ""
    text = text.replace('♀', '')
    text = ''.join([c if c.isalnum() else ' ' for c in text])
    text = text.strip()
    text = ' '.join(text.split())

    return text

def save_location():
    with open('location_coordinates.txt', 'r') as f:
        location_coordinates = json.loads(f.read())
    location_text = ocr_region(location_coordinates, save_screenshot=True, screenshot_path="location_screenshot.png")
    location_list = []
    if os.path.exists('location_list.txt'):
        with open('location_list.txt', 'r') as f:
            location_list = json.loads(f.read())
    location_list.append(location_text)
    if len(location_list) > 5:
        location_list.pop(0)
    with open('location_list.txt', 'w') as f:
        f.write(json.dumps(location_list))

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
