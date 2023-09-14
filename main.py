# @Dimitry Ermakov
# @09/09/2023
import re
import sys
import threading
import time
from datetime import datetime

import keyboard
import pyautogui
import pytesseract

# Constants
EXIT_CODE = "-1"
DEFAULT_PROMPT = "0"
ESCAPE_KEY = "esc"
MEDIUM_DELAY = 0.25
LONG_DELAY = 1  # 0.77

noted_date = "1/"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = LONG_DELAY

current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")


def cord_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    if keyboard.is_pressed(ESCAPE_KEY):
        print("Escape key pressed. Stopping the program.")
        sys.exit()


def get_to_dead_page():
    cord_click(271, 228)  # click on the search bar
    time.sleep(1.25)
    cord_click(290, 377)  # click on constituents updates
    time.sleep(5)
    cord_click(320, 490)  # click on the first constituent


def click_on_first_interaction():
    cord_click(424, 789)  # click on first pending
    time.sleep(0.5)
    cord_click(300, 822)  # click on the edit button
    time.sleep(2)


def is_text_empty(text):
    # Check if the text is None or consists only of whitespace characters
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False


def contains_date(text):
    # Regular expression pattern to match YYYY or MM/YYYY format dates
    date_pattern = r"\b(\d{4}|\d{1,2}/\d{4})\b"

    # Search for the pattern in the text
    match = re.search(date_pattern, text)

    # If a match is found, return True; otherwise, return False
    if match:
        return True
    else:
        return False


def confirm():
    global noted_date
    time.sleep(0.75)
    cord_click(687, 250)
    cord_click(535, 297)
    cord_click(1022, 337)
    cord_click(924, 526)
    found_text = extract_text_from_coordinates(750, 1050, 2100, 1300)
    if contains_date(found_text) is True and "year" in found_text is False:
        noted_date = pyautogui.prompt(text="", title="Noted Date?", default="1/")
        cord_click(444, 444)
    time.sleep(1)
    cord_click(1035, 617)
    if is_text_empty(found_text) == False:
        pyautogui.press("enter")
        pyautogui.press("enter")
    keyboard.write("Note: Not Researched - DE")
    time.sleep(MEDIUM_DELAY)
    cord_click(857, 826)
    time.sleep(MEDIUM_DELAY)
    cord_click(912, 828)  # save button
    # cord_click(1015, 825)  # cancel button


def decline(num):
    # form
    time.sleep(2)
    cord_click(687, 252)
    cord_click(523, 338)
    cord_click(1023, 338)
    cord_click(924, 526)
    cord_click(1035, 635)
    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - DE")
    time.sleep(0.05)
    cord_click(857, 826)
    time.sleep(0.3)
    cord_click(912, 828)  # save button
    # cord_click(1015, 825)  # cancel button
    if num <= 3:
        return DEFAULT_PROMPT
    elif num > 3:
        time.sleep(0.5)
        end = pyautogui.prompt(
            text="", title="More duplicates?, 1 = yes, 0 = no", default=DEFAULT_PROMPT
        )
        cord_click(194, 664)  # safe corner
        time.sleep(0.5)
    return end


def deceased_form():
    global noted_date
    cord_click(716, 458)  # date
    if noted_date == "1/":
        keyboard.write(formatted_date)
    elif noted_date != "1/":
        keyboard.write(noted_date)
    cord_click(857, 514)
    cord_click(772, 562)  # reason
    time.sleep(MEDIUM_DELAY)
    cord_click(736, 571)  # save button
    # cord_click(834, 579)  # cancel button


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    # textbox_image.show()
    # textbox_image.save("textbox.png")
    extracted_text = pytesseract.image_to_string(textbox_image)
    # print(extracted_text.strip())
    return extracted_text.strip()


def move_to_communications():
    cord_click(73, 370)  # consituents
    time.sleep(6)
    cord_click(497, 826)  # communications


def opt_out_form():
    time.sleep(MEDIUM_DELAY)
    cord_click(703, 442)
    time.sleep(0.5)
    keyboard.write("Imprimis")
    time.sleep(0.5)
    cord_click(572, 442)  # wait
    time.sleep(0.5)
    cord_click(850, 505)  # date button
    cord_click(748, 686)  # today
    cord_click(850, 476)  # tab
    cord_click(733, 515)  # opt out
    # cord_click(698, 642)
    # time.sleep(1)
    cord_click(849, 637)  # tab
    time.sleep(MEDIUM_DELAY)
    cord_click(698, 706)  # deceased press
    cord_click(636, 642)
    down_command(3)
    cord_click(737, 820)  # save
    # cord_click(272, 225)  # click on the search bar


def down_command(num):
    for _ in range(0, num):
        pyautogui.press("down")


def interactions_section(num):
    time.sleep(5)
    down_command(6)
    time.sleep(MEDIUM_DELAY)
    click_on_first_interaction()

    if num == 1:
        confirm()
        time.sleep(1.75)
        cord_click(286, 587)  # personal info click
        time.sleep(1)
        cord_click(531, 685)  # mark deceased button
        time.sleep(1)
    elif num == 2:
        confirm()
        time.sleep(2)
        cord_click(415, 815)  # click on the second pending
        time.sleep(1.5)
        cord_click(298, 837)  # click on second edit button
        decline(num)
        time.sleep(1.75)
        cord_click(286, 587)  # personal info click
        time.sleep(1)
        cord_click(531, 685)  # mark deceased button
        time.sleep(1)
    elif num == 3:
        confirm()
        time.sleep(1.5)
        cord_click(415, 815)  # click on the second pending
        time.sleep(1)
        cord_click(298, 837)  # click on second edit button
        decline(num)
        time.sleep(1)
        down_command(2)
        time.sleep(1)
        cord_click(418, 756)  # click on the third pending
        time.sleep(1)
        cord_click(291, 792)  # click on the third edit
        decline(num)
        time.sleep(1.5)
        cord_click(278, 387)  # personal info click
        time.sleep(1)
        cord_click(545, 488)  # mark deceased button
        time.sleep(1)
    elif num > 3:
        confirm()
        time.sleep(1)
        duplicates = True
        while duplicates:
            pyautogui.prompt(
                text="",
                title="Enter when you are at the decline form",
                default=DEFAULT_PROMPT,
            )
            cord_click(857, 826)
            if decline(num) == DEFAULT_PROMPT:
                duplicates = False
            pyautogui.prompt(
                text="",
                title="Enter when you are at the deceased form",
                default=DEFAULT_PROMPT,
            )
            cord_click(639, 515)  # wait
            time.sleep(1)


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


def main():
    job = pyautogui.prompt(
        text="", title="Enter the Task, -1 to quit", default=DEFAULT_PROMPT
    )
    if job == EXIT_CODE:
        sys.exit()
    cord_click(271, 173)
    while job != EXIT_CODE and keyboard.is_pressed(ESCAPE_KEY) is False:
        start_time = time.time()
        get_to_dead_page()
        time.sleep(5)
        num = int(
            extract_digits_from_text(
                extract_text_from_coordinates(420, 1350, 620, 1400)
            )
        )
        time.sleep(MEDIUM_DELAY)
        cord_click(262, 691)  # interactions button
        interactions_section(num)
        deceased_form()
        time.sleep(3)
        move_to_communications()
        down_command(2)
        time.sleep(MEDIUM_DELAY)
        cord_click(382, 822)  # click on add for communications
        opt_out_form()
        time.sleep(5)
        end_time = time.time()
        duration = end_time - start_time
        log_file = "program_log.txt"
        with open(log_file, "a") as f:
            f.write(f"Program execution time: {duration:.2f} seconds\n")


if __name__ == "__main__":
    threading.Thread(target=keyboard.wait, args=(ESCAPE_KEY,)).start()
    main()
