import pyautogui
import pytesseract
import re
from datetime import datetime


def remove_numbers_greater_than_current_year(input_text):
    current_year = datetime.now().year
    # Regular expression pattern to match numbers in the input text
    number_pattern = r"\b\d+\b"

    def remove_numbers(match):
        number = int(match.group(0))
        if number <= current_year:
            return str(number)
        else:
            return ""

    return re.sub(number_pattern, remove_numbers, input_text)


def remove_phone_numbers(text):
    phone_pattern = (
        r"\b(\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4})\b"
    )
    return re.sub(phone_pattern, "", text)


def remove_digits_next_to_letters(input_string):
    return re.sub(r"([a-zA-Z])\d+|\d+([a-zA-Z])", r"\1\2", input_string)


def extract_text_from_coordinates(x1, y1, x2, y2):
    # Path to the Tesseract executable, may need to use path to the .exe file depending on the operating system
    # path_to_tesseract = "tesseract.exe"
    # pytesseract.tesseract_cmd = path_to_tesseract

    # Capture the current screen as a screenshot
    screenshot = pyautogui.screenshot()

    # Crop the screenshot to the specified coordinates
    textbox_image = screenshot.crop((x1, y1, x2, y2))

    # Use Tesseract to extract text from the cropped image
    extracted_text = pytesseract.image_to_string(textbox_image)

    # Return the extracted text after stripping any leading/trailing whitespace
    return extracted_text.strip()


def cord_click(coordinates):
    # Move the mouse pointer to the specified coordinates
    pyautogui.moveTo(coordinates[0], coordinates[1])

    # Perform a mouse click at the current position
    pyautogui.click()


def tab_command(number_of_interactions):
    # Simulate pressing the "Tab" key a specified number of times
    for _ in range(0, number_of_interactions):
        pyautogui.press("tab")


def extract_digits_from_text(text):
    # Filter and join only the digits from the input text
    return "".join(filter(str.isdigit, text))


def is_text_empty(text):
    # Check if the text is None or contains only whitespace
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False
