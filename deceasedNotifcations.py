# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime
import pygame
import pyperclip
import keyboard
import pyautogui
from pytesseract import pytesseract
import re
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime


from main_shared_functions import (
    extract_text_from_coordinates,
    cord_click,
    tab_command,
    extract_digits_from_text,
    extract_date,
    remove_numbers_greater_than_current_year,
    remove_phone_numbers,
    remove_digits_next_to_letters,
)


# original_x_scale = 1440 / 2880
# original_y_scale = 900 / 1800

x_scale = 1
y_scale = 1
delay = 0.05
confidence = 0.7
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900
pyautogui.FAILSAFE = True
pyautogui.PAUSE = delay
PRIMARY_EMAIL = "windowsTarget/primary_email.png"
MAX_ATTEMPTS = round(1.25 / (delay * 5))
CURRENT_DATE = datetime.now()
formatted_month = str(CURRENT_DATE.month)
formatted_year = str(CURRENT_DATE.year)
formatted_day = str(CURRENT_DATE.day)
FORMATTED_DATE = f"{formatted_month}/{formatted_year}"
FULL_DATE = f"{formatted_month}/{formatted_day}/{formatted_year}"


def find_and_click_image(image_filename, biasx=0, biasy=0, up_or_down=None):
    global cutOffTopY, delay, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, confidence, PRIMARY_EMAIL, IMPRIMIS, EDUCATION, LOAD_OPT_OUT_WAIT, LOAD_OWNER_WAIT

    box = None
    # Loop until a valid bounding box is found
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),
            ),
        )
        time.sleep(delay * 5)
        # If the image is not found and 'up_or_down' is specified
        if box is None and up_or_down:
            # Scroll the screen up or down based on 'up_or_down'
            factor = 14 if up_or_down == "up" else -14
            pyautogui.scroll(factor)
            time.sleep(delay * 2)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy

    cord_click((x, y))


def end_time_recording(start_time):
    end_time = time.time()
    duration = end_time - start_time
    log_file = "time_logs/notifcationsLog.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    global delay, MAX_ATTEMPTS, x_scale, y_scale, confidence
    box = None
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(delay * 5)
    _, y, width, height = box
    image_cords_x = (box.left) + width / 2
    image_cords_y = (box.top) + height / 2
    return round(y), (image_cords_x, image_cords_y)


def main():
    global initials, cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, EDUCATION, COM_NUM, delay, PRIMARY_EMAIL
    input_str = pyautogui.prompt(
        text="Enter date if there is one and then LookUp ID or full name (ex - Elizabeth W. Clenio)",
        # tab 9 for address, name ex - Elizabeth W. Clenio
        title="date, name, or LookUp ID",
        default=f"{FULL_DATE},",
    )
    givendate, lookup_id_or_name = input_str.strip().split(",")
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while initials != "-1":
        start_time = time.time()
        find_and_click_image("windowsTarget/constituteSearch.png")
        time.sleep(delay * 5)
        find_and_click_image("windowsTarget/nameOrLookUpID.png")
        keyboard.write(lookup_id_or_name)
        pyautogui.press("enter")
        time.sleep(delay * 5)
        find_and_click_image("windowsTarget/cityStateZIP.png", 0, round(25 * y_scale))
        time.sleep(delay * 5)
        find_and_click_image(PRIMARY_EMAIL)
        find_and_click_image("windowsTarget/deceasedNotification.png")
        time.sleep(delay * 5)
        find_and_click_image("windowsTarget/comments.png")
        pyautogui.press("tab")
        keyboard.write(f"Passed away {givendate}")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")

        end_time_recording(start_time)
        find_and_click_image(PRIMARY_EMAIL)


#  windowsTarget/comments.png             | Bin 0 -> 1025 bytes
#  windowsTarget/deceasedNotification.png | Bin 0 -> 1932 bytes
if __name__ == "__main__":
    main()
