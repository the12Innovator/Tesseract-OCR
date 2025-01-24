import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import time
import keyboard
import csv
import re

# Set up Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Paths
input_csv_path = r"C:\Users\Lenovo\OneDrive\Documents\Projects\Python\Tesseract-OCR\Groww_Fun\Sorted_stocks.csv"
output_csv_path = r"C:\Users\Lenovo\OneDrive\Documents\Projects\Python\Tesseract-OCR\Groww_Fun\fundamentals_data.csv"
screenshot_path = r"C:\Users\Lenovo\OneDrive\Documents\Projects\Python\Tesseract-OCR\Groww_Fun\Screenshot.png"

# OCR Region for fundamentals data (update coordinates as required)
ocr_region = (960, 130, 1760 - 960, 900 - 130)  # x, y, width, height

# Global pause flag
paused = False

# Function to toggle pause/resume with a dialogue box
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Program paused. Please resume from the dialogue box.")
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        response = messagebox.askyesno("Pause", "Program paused. Resume?")
        if response:  # User clicks "Yes"
            paused = False
        else:  # User clicks "No"
            print("Exiting program...")
            root.destroy()
            exit()

# Add hotkey for pause/resume
keyboard.add_hotkey('ctrl+alt', toggle_pause)

# Read stock names from CSV
def get_stock_names(file_path):
    df = pd.read_csv(file_path)
    stock_names = df.iloc[1:29, 0].tolist()
    return stock_names

# Automate Groww website navigation
def automate_search(stock_name):
    pag.click(x=1525, y=138)  # Click on the search bar
    time.sleep(1)
    pag.typewrite(stock_name, interval=0.1)
    time.sleep(2)
    pag.click(x=1449, y=235)  # Select the stock
    time.sleep(2)
    pag.scroll(-1500)  # Scroll down to fundamentals
    time.sleep(2)

# Capture screenshot of fundamentals data
def capture_fundamentals():
    screenshot = pag.screenshot(region=ocr_region)
    screenshot.save(screenshot_path)
    return screenshot

# Process image using Tesseract OCR
def analyze_image(image):
    img = image.convert("L")  # Convert to grayscale
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image
    img = ImageEnhance.Contrast(img).enhance(2)  # Enhance contrast
    config = r"--psm 6"  # Assume uniform block of text
    text = pytesseract.image_to_string(img, config=config)
    return text

# Extract specific data fields from OCR text using regex
def extract_fundamentals(text):
    try:
        data = {
            "Market Cap": re.search(r"Market Cap\s([\S]+)", text),
            "ROE": re.search(r"ROE\s([\S]+)", text),
            "P/B Ratio": re.search(r"P/B Ratio\s([\S]+)", text),
            "Debt to Equity": re.search(r"Debt to Equity\s([\S]+)", text)
        }
        extracted_data = {key: (match.group(1) if match else "N/A") for key, match in data.items()}
        return extracted_data
    except Exception as e:
        print(f"Error parsing OCR text: {e}")
        return None

# Write data to CSV
def write_to_csv(data):
    with open(output_csv_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Stock Name", "Market Cap", "ROE", "P/B Ratio", "Debt to Equity"
        ])
        writer.writerow(data)

# Display extracted data in terminal
def display_in_terminal(stock_name, data, added):
    print(f"\nProcessing stock: {stock_name}")
    print("-" * 50)
    for key, value in data.items():
        print(f"{key}: {value}")
    print("-" * 50)
    if added:
        print(f"Stock '{stock_name}' meets the criteria and has been added.")
    else:
        print(f"Stock '{stock_name}' does not meet the criteria and has been skipped.")
    print("-" * 50)

# Main process
def process_stocks():
    stock_names = get_stock_names(input_csv_path)

    # Initialize output CSV with headers
    with open(output_csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Stock Name", "Market Cap", "ROE", "P/B Ratio", "Debt to Equity"
        ])
        writer.writeheader()

    for stock_name in stock_names:
        # Pause handling
        while paused:
            time.sleep(0.1)

        automate_search(stock_name)
        screenshot = capture_fundamentals()
        text = analyze_image(screenshot)

        data = extract_fundamentals(text)
        if data:
            data["Stock Name"] = stock_name

            try:
                roe = float(data["ROE"].replace("%", "").replace(",", "")) if data["ROE"] != "N/A" else -1
                pb_ratio = float(data["P/B Ratio"].replace(",", "")) if data["P/B Ratio"] != "N/A" else float("inf")
                debt_to_equity = float(data["Debt to Equity"].replace(",", "")) if data["Debt to Equity"] != "N/A" else float("inf")

                if roe >= 15 and pb_ratio <= 3 and debt_to_equity < 1:
                    write_to_csv(data)
                    display_in_terminal(stock_name, data, True)
                else:
                    display_in_terminal(stock_name, data, False)
            except ValueError:
                print(f"Failed to parse numeric data for {stock_name}. Skipping.")
        else:
            print(f"Failed to parse data for {stock_name}.")

        pag.scroll(1500)
        time.sleep(1)
        pag.click(x=1782, y=134)
        time.sleep(1)

# Run the script
if __name__ == "__main__":
    process_stocks()
