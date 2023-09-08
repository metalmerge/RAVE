import pyautogui
import pytesseract
from PIL import Image


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    pyautogui.prompt(
        text="Press OK when you are ready to capture the textbox.",
        title="Capture Textbox",
    )
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    # textbox_image.show()
    extracted_text = pytesseract.image_to_string(textbox_image)
    return extracted_text.strip()


# Define the screen coordinates you obtained
x1, y1 = 420, 1350  # Replace with the top-left coordinates
x2, y2 = 620, 1400  # Replace with the bottom-right coordinates
print(extract_text_from_coordinates(x1, y1, x2, y2))
