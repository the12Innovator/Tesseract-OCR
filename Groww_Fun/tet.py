#The program preprocesses an image, extracts text using Tesseract OCR, filters relevant text, and parses it into key-value pairs for structured output.
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# Set up Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to the image
image_path = r"C:\Users\Lenovo\OneDrive\Documents\Projects\Python\Tesseract-OCR\Groww_Fun\Screenshot copy.png"

def extract_text_from_image(image_path):
    try:
        # Open the image
        img = Image.open(image_path)

        # Preprocess the image
        img = img.convert("L")  # Convert to grayscale
        img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image
        img = ImageEnhance.Contrast(img).enhance(2)  # Enhance contrast

        # Extract text using Tesseract
        config = r"--psm 6"  # Assume a uniform block of text
        text = pytesseract.image_to_string(img, config=config)

        # Extract text between "Fundamentals" and "Understand Fundamentals"
        start_index = text.find("Fundamentals")
        end_index = text.find("Understand Fundamentals")

        if start_index != -1 and end_index != -1:
            relevant_text = text[start_index + len("Fundamentals"):end_index].strip()
        else:
            relevant_text = text  # Use the entire text if markers are not found

        # Parse data line by line into key-value pairs
        parsed_data = {}
        lines = relevant_text.split("\n")

        for line in lines:
            # Split by first space for key-value extraction
            if " " in line:
                key, value = line.split(" ", 1)
                parsed_data[key.strip()] = value.strip()

        print("Relevant Extracted Text:")
        print("-" * 50)
        print(relevant_text)
        print("-" * 50)

        print("Parsed Data:")
        for key, value in parsed_data.items():
            print(f"{key}: {value}")
        return parsed_data

    except Exception as e:
        print(f"Error processing the image: {e}")
        return None

# Call the function
extract_text_from_image(image_path)
