import keyboard

# Define the key to start and stop recording
record_key = 'r'

# List to store recorded actions
recorded_actions = []

# Flag to indicate whether recording is in progress
recording = False

def on_key_press(event):
    global recording
    global recorded_actions
    
    if event.name == record_key:
        recording = not recording
        if recording:
            recorded_actions.clear()
            print("Started recording")
        else:
            print("Stopped recording")

    # If recording is in progress, record the key press
    if recording:
        recorded_actions.append(event.name)
    
# Start the listener to monitor keypresses
keyboard.on_press(on_key_press)

print(f"Press '{record_key}' to start/stop recording.")

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

print("Recorded actions:")
print(recorded_actions)
