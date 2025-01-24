#Find Mouse Position
from pynput.mouse import Listener
import os

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display mouse position
def on_move(x, y):
    clear_console()
    print(f"Mouse position: x={x}, y={y}")

# Function to handle exiting the listener
def on_click(x, y, button, pressed):
    if not pressed:  # Stop when you release a mouse button
        print("Stopped tracking.")
        return False

# Run the mouse listener
with Listener(on_move=on_move, on_click=on_click) as listener:
    listener.join()

