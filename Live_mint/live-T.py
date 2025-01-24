import pyautogui as pag
import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import time
import keyboard

# Set up Tesseract OCR path (update this with your Tesseract path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Paths
excel_path = r"C:\Users\Lenovo\OneDrive\Documents\Projects\Python\Tesseract-OCR\Live_mint\Selected_stocks.xlsx"
image_path = r"C:\Users\Lenovo\OneDrive\Documents\Projects\Python\Tesseract-OCR\Live_mint\Screenshot 2025-01-01 174558.png"

# Function to extract stock names from Excel
def get_stock_names(file_path):
    df = pd.read_excel(file_path)
    stock_names = df.iloc[0:89, 2].dropna().tolist()  # Adjusted for range C2 to C76
    return df, stock_names

# Function to automate search and capture screenshots
def automate_search(stock_name):
    # Click on the search bar
    pag.click(x=1824, y=129)
    pag.typewrite(stock_name, interval=0.1)
    time.sleep(2)  # Wait for suggestions to appear

    # Select the suggested stock name
    pag.click(x=1035, y=295)
    time.sleep(2)

    # Scroll down to reveal the image
    pag.scroll(-1500)  # Adjust based on your webpage layout
    time.sleep(2)

    # Take a screenshot of the specific area (adjust coordinates as needed)
    screenshot = pag.screenshot(region=(900, 400, 950, 400))  # Example region
    screenshot.save(image_path)
    time.sleep(2)

# Function to preprocess and analyze the screenshot using Tesseract OCR
def analyze_image(image_path):
    try:
        # Preprocessing the image
        img = Image.open(image_path).convert("L")  # Convert to grayscale
        img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image
        img = ImageEnhance.Contrast(img).enhance(2)  # Enhance contrast

        # Run OCR
        config = r"--psm 6"  # Assume a uniform block of text
        text = pytesseract.image_to_string(img, config=config)

        if "Balanced risk" in text and "Strong Buy" in text:
            return True
    except Exception as e:
        print(f"Error analyzing image: {e}")
    return False

# Global pause flag
paused = False

# Function to toggle the pause state
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Program paused. Press 'p' to resume.")
    else:
        print("Resuming...")

# Add hotkey for pause/resume
keyboard.add_hotkey('p', toggle_pause)

# Main process function
def process_stocks():
    df, stock_names = get_stock_names(excel_path)
    total_stocks = len(stock_names)

    removed_stocks = 0
    added_stocks = 0

    for idx, stock in enumerate(stock_names, start=1):
        print(f"Processing {idx}/{total_stocks}: {stock}")

        # Check for pause
        while paused:
            time.sleep(0.1)

        # Automate the search process
        automate_search(stock)

        # Analyze the captured image
        meets_condition = analyze_image(image_path)

        # Remove stock if conditions are not met
        if not meets_condition:
            df = df[df.iloc[:, 2] != stock]
            removed_stocks += 1
            print(f"Removed {stock} as it does not meet the conditions.")
        else:
            added_stocks += 1
            print(f"Added {stock} to the list as it meets the conditions.")

    # Save updated DataFrame to Excel
    df.to_excel(excel_path, index=False)
    print("Process completed. Excel file updated.")

    # Summary
    print(f"\nSummary:")
    print(f"Total stocks processed: {total_stocks}")
    print(f"Stocks removed: {removed_stocks}")
    print(f"Stocks added: {added_stocks}")

# Run the process once
if __name__ == "__main__":
    process_stocks()
