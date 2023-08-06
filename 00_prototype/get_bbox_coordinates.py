import os
import tkinter as tk
import json

# The coordinates of the bounding box for death_coordinates
death_coordinates = []

def on_click(event):
    # Record the coordinates when the mouse button is pressed
    death_coordinates.append((event.x, event.y))

def on_release(event):
    # Record the coordinates when the mouse button is released
    death_coordinates.append((event.x, event.y))

    # Save the coordinates to death_coordinates file
    with open('death_coordinates.txt', 'w') as f:
        f.write(json.dumps(death_coordinates))

    # Quit the program after the box has been drawn
    root.quit()

if not os.path.exists('death_coordinates.txt'):
    root = tk.Tk()
    root.attributes('-fullscreen', True, '-alpha', 0.3)

    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()

# The coordinates of the bounding box for location_coordinates
location_coordinates = []

def on_click(event):
    # Record the coordinates when the mouse button is pressed
    location_coordinates.append((event.x, event.y))

def on_release(event):
    # Record the coordinates when the mouse button is released
    location_coordinates.append((event.x, event.y))

    # Save the coordinates to location_coordinates file
    with open('location_coordinates.txt', 'w') as f:
        f.write(json.dumps(location_coordinates))

    # Quit the program after the box has been drawn
    root.quit()

if not os.path.exists('location_coordinates.txt'):
    root = tk.Tk()
    root.attributes('-fullscreen', True, '-alpha', 0.3)

    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()
