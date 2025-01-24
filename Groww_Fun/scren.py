#This program takes screen from (start_x, start_y) to (end_x, end_y) coordinate
import pyautogui as pag
from datetime import datetime

# Coordinates of the region to capture (x, y, width, height)
start_x, start_y = 960, 130
end_x, end_y = 1760, 900

# Calculate the width and height of the region
width = end_x - start_x
height = end_y - start_y

# Function to capture a screenshot of the specified region
def capture_screenshot():
    # Take a screenshot of the region
    screenshot = pag.screenshot(region=(start_x, start_y, width, height))
    
    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the screenshot
    filename = f"test_{timestamp}.png"
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

# Call the function
if __name__ == "__main__":
    capture_screenshot()


