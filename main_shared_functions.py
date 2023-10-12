import pyautogui
import pytesseract
import re
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime


def extract_date(input_text):
    months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    day_month_year_result = day_month_year_only(input_text)
    if day_month_year_result is not None:
        return day_month_year_result
    month_year_result = month_year_only(input_text, months)
    if month_year_result is not None:
        return month_year_result
    year_only_result = year_only(input_text)
    if year_only_result is not None:
        return year_only_result

    # Regular expression pattern to match different date formats.
    date_pattern = r"\b(\d{1,2})[ /-](\d{4})\b|\b([A-Za-z]+)[ /-](\d{4})\b"
    matches = re.findall(date_pattern, input_text)

    if matches:
        for match in matches:
            if match[0]:  # Matched day and year (e.g., 10/2023 or 10-2023)
                month, year = match[0], match[1]
                return f"{month}/{year}"
            elif match[2] in months:  # Check if the matched text is a valid month name
                month, year = months[match[2]], match[3]
                return f"{month}/{year}"

    # Handle the case of "month YYYY"
    month_year_pattern = r"\b([A-Za-z]+) (\d{4})\b"
    month_year_match = re.search(month_year_pattern, input_text)
    if month_year_match:
        month, year = months[month_year_match.group(1)], month_year_match.group(2)
        return f"{month:02d}/{year}"

    # Handle special cases for phrases like "last month," "last year," and "this year."
    return special_cases(input_text)


def day_month_year_only(input_text):
    date_pattern = r"\b(\d{1,2})[ /-](\d{1,2})[ /-](\d{4})\b"
    matches = re.findall(date_pattern, input_text)
    if matches:
        for match in matches:
            month, year = match[0], match[2]
            if month.startswith("0"):
                month = month[1]  # Remove leading zero
            return f"{month}/{year}"
    return None


def year_only(input_text):
    year_pattern = r"\b(\d{4})\b"
    year_match = re.search(year_pattern, input_text)
    if year_match:
        year = year_match.group(1)
        return f"1/{year}"
    return None


def month_year_only(input_text, months):
    month_year_pattern = r"\b([A-Za-z]+)[ /-](\d{4})\b"
    month_year_match = re.search(month_year_pattern, input_text)
    if month_year_match:
        month = months.get(month_year_match.group(1))
        year = month_year_match.group(2)
        if month:
            return f"{month}/{year}"
    return None


def special_cases(input_text):
    CURRENT_DATE = datetime.now()
    formatted_month = str(CURRENT_DATE.month)
    formatted_year = str(CURRENT_DATE.year)
    if "last month" in input_text:
        last_month = int(formatted_month) - 1
        return f"{last_month}/{formatted_year}"

    if "last year" in input_text:
        last_year = int(formatted_year) - 1
        return f"1/{last_year}"

    if "this year" in input_text:
        return f"1/{formatted_year}"
    if "this month" in input_text:
        return f"{formatted_month}/{formatted_year}"

    return "1/"


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
