import os
import tkinter as tk
import pyautogui
import json
import pytesseract
import pyperclip
import time

# The coordinates of the bounding box
coordinates = []

def on_click(event):
    # Record the coordinates when the mouse button is pressed
    coordinates.append((event.x, event.y))

def on_release(event):
    # Record the coordinates when the mouse button is released
    coordinates.append((event.x, event.y))

    # Save the coordinates to a file
    with open('coordinates.txt', 'w') as f:
        f.write(json.dumps(coordinates))

    # Quit the program after the box has been drawn
    root.quit()

if not os.path.exists('coordinates.txt'):
    root = tk.Tk()
    root.attributes('-fullscreen', True, '-alpha', 0.3)

    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()

# Load the coordinates
with open('coordinates.txt', 'r') as f:
    coordinates = json.loads(f.read())

# Set the path to the tesseract executable
# You may need to adjust this path depending on your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Continuously screenshot the area, perform OCR, and copy the results to the clipboard
while True:
    x1, y1 = coordinates[0]
    x2, y2 = coordinates[1]
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    text = pytesseract.image_to_string(screenshot)
    if text != '' and text != '':
        print(text)
        pyperclip.copy(text)
    

    # Sleep for a bit to avoid overwhelming your system
    time.sleep(2)
