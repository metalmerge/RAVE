import pyautogui
import pytesseract
import re
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime


def detect_dates(input_text):
    # Define a list of common date formats as regular expressions
    date_formats = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
        r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
        r"\d{2}-\d{2}-\d{4}",  # MM-DD-YYYY
        r"\d{2}/\d{2}/\d{2}",  # MM/DD/YY
        r"\d{1,2}-[A-Za-z]{3}-\d{4}",  # DD-Mon-YYYY (e.g., 15-Jan-2023)
        r"\d{1,2} [A-Za-z]{3} \d{4}",  # DD Mon YYYY (e.g., 15 Jan 2023)
        r"[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember",  # Month names
    ]

    # Combine the date format regular expressions into a single pattern
    date_pattern = "|".join(date_formats)

    # Use regular expression to find all matching dates in the input text
    matched_dates = re.findall(date_pattern, input_text)

    # Parse the matched dates using dateutil.parser and format them
    DATE_FORMAT = "%-m/%Y"
    formatted_dates = []

    for date_str in matched_dates:
        try:
            parsed_date = parse(date_str)
            formatted_date = parsed_date.strftime(DATE_FORMAT)
            formatted_dates.append(formatted_date)
        except ValueError:
            # Handle parsing errors (e.g., invalid date strings)
            pass

    # Handle phrases like "last month," "next month," "last year," and "this year"
    if re.search(r"\b[Ll]ast [Mm]onth\b", input_text):
        last_month = datetime.now() - relativedelta(months=1)
        formatted_dates[0] = last_month.strftime(DATE_FORMAT)
    if re.search(r"\b[Nn]ext [Mm]onth\b", input_text):
        next_month = datetime.now() + relativedelta(months=1)
        formatted_dates[0] = next_month.strftime(DATE_FORMAT)
    if re.search(r"\b[Ll]ast [Yy]ear\b", input_text):
        last_year = datetime.now() - relativedelta(years=1)
        formatted_dates[0] = last_year.strftime(DATE_FORMAT)
    if re.search(r"\b[Tt]his [Yy]ear\b", input_text):
        this_year = datetime.now()
        formatted_dates[0] = this_year.strftime(DATE_FORMAT)

    # Add the current month and year by default if no other dates are detected
    if not formatted_dates:
        formatted_dates.append(datetime.now().strftime(DATE_FORMAT))

    return formatted_dates[0]


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
