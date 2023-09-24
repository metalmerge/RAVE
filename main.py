# @Dimitry Ermakov
# @09/23/2023
import re
import time
from datetime import datetime
import keyboard
import pyautogui
import pytesseract
import os

# Interactions: 2 = 79.14 bot; 75.66 no copy pasting, experienced, fast as possible human
# Interactions: 1 = 55.25 bot; 51.08 no copy pasting, experienced, fast as possible human

# TODO get ride of needing biasX and biasY, fix extract_text_from_coordinates hard coded coordinates
# TODO change more find_and_click_image to tabbing
# text_comment scanner did not work
# prompt for screen size
# reform num > 3
# get sound for notifications
# tab more
# up and down commands to relate to screen size

DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
pyautogui.FAILSAFE = True
DELAY = 0.05
pyautogui.PAUSE = DELAY
MAX_ATTEMPTS = round(1 / DELAY)
x_scale = 1
y_scale = 1
# x_scale = 1440 / 2880
# y_scale = 900 / 1800

current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")
full_date = current_date.strftime("%-m/%-d/%Y")
PRIMIS = "target/receives_imprimis.png"
CRM = "target/blackbaud_CRM.png"

import time


def find_and_click_image(image_filename, biasx, biasy):
    try:
        box = None
        attempts = 0
        while box is None:
            box = pyautogui.locateOnScreen(image_filename, confidence=0.9)
            time.sleep(DELAY)
            print("Searching for image: " + image_filename)

            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                os.system(
                    "osascript -e 'display notification \"Image not found after "
                    + str(MAX_ATTEMPTS)
                    + ' attempts" with title "Failed to find Image" sound name "Glass"\''
                )

                break

        x, y, width, height = box
        x = box.left * 0.5 + width / 4 + biasx
        y = box.top * 0.5 + height / 4 + biasy
        if (
            image_filename != PRIMIS
            and image_filename != "target/receives_imprimis.png"
            and image_filename != "target/wait_for_load_opt_out.png"
        ):
            pyautogui.moveTo(x, y)
            pyautogui.click()

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def up_command(num):
    for _ in range(0, num):
        pyautogui.press("up")


def tab_command(num):
    for _ in range(0, num):
        pyautogui.press("tab")


def down_command(num):
    for _ in range(0, num):
        pyautogui.press("down")


def contains_digits(text):
    pattern = r"\d"
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


def get_to_dead_page():
    find_and_click_image("target/constituents.png", 0, 0)
    find_and_click_image("target/updates.png", 0, 0)
    find_and_click_image("target/name.png", 0, 25)


def click_on_top_interaction(num):
    STATUS = "target/status_alone.png"
    find_and_click_image(STATUS, 0, (num * 30))
    find_and_click_image("target/edit_interaction.png", 0, 0)


def interactions_section(num):
    global CRM, PRIMIS
    OWNER = "target/wait_for_owner.png"
    find_and_click_image("target/interactions.png", 0, 0)
    find_and_click_image(PRIMIS, 0, 0)
    down_command(num * 2 + 8)
    click_on_top_interaction(1)
    confirm()
    if num == 2:
        find_and_click_image(OWNER, 0, 0)
        # down_command(num)
        click_on_top_interaction(num)
        decline(num)

    elif num == 3:
        find_and_click_image(OWNER, 0, 0)
        # down_command(num - 1)
        click_on_top_interaction(num - 1)  # starts at 2 always
        decline(num)
        find_and_click_image(OWNER, 0, 0)
        # down_command(num - 2)
        click_on_top_interaction(num)
        decline(num)

    elif num > 3:
        confirm()

        duplicates = True
        while duplicates:
            pyautogui.prompt(
                text="",
                title="Enter when you are at the decline form",
                default=DEFAULT_PROMPT,
            )
            find_and_click_image(CRM, 0, 0)
            if decline(num) == DEFAULT_PROMPT:
                duplicates = False
    up_command(num * 3)
    get_to_mark_deceased()


def is_text_empty(text):
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False


def confirm():
    global noted_date, initials, full_date

    find_and_click_image("target/tab_down_complete.png", 0, 0)
    find_and_click_image("target/completed_form.png", 0, 0)
    tab_command(7)
    keyboard.write(full_date)
    found_text = extract_text_from_coordinates(750, 1050, 2100, 1300)
    if (
        contains_digits(found_text) is True
        and "year" not in found_text
        and "month" not in found_text
    ):
        noted_date = pyautogui.prompt(text="", title="Noted Date?", default="1/")
        find_and_click_image("target/sites.png", 0, 0)
    tab_command(3)
    if is_text_empty(found_text) == False:
        pyautogui.press("enter")
        pyautogui.press("enter")
    keyboard.write("Note: Not Researched - " + initials)
    tab_command(2)
    pyautogui.press("enter")


def decline(num):
    global initials, CRM
    find_and_click_image("target/tab_down_complete.png", 0, 0)
    find_and_click_image("target/declined.png", 0, 0)
    tab_command(7)
    keyboard.write(full_date)
    tab_command(3)

    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - " + initials)
    tab_command(2)
    pyautogui.press("enter")

    if num <= 3:
        return DEFAULT_PROMPT
    elif num > 3:
        end = pyautogui.prompt(
            text="", title="More duplicates?, 1 = yes, 0 = no", default=DEFAULT_PROMPT
        )
        find_and_click_image(CRM, 0, 0)

    return end


def deceased_form():
    global noted_date
    find_and_click_image("target/deceased_date.png", 0, 0)
    if noted_date == "1/":
        keyboard.write(formatted_date)
    elif noted_date != "1/":
        keyboard.write(noted_date)
    find_and_click_image("target/source_tab_down.png", 0, 0)
    find_and_click_image("target/communication_from.png", 0, 0)
    pyautogui.press("enter")


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    extracted_text = pytesseract.image_to_string(textbox_image)
    print(extracted_text.strip())
    return extracted_text.strip()


def move_to_communications():
    global PRIMIS
    find_and_click_image("target/constitute.png", 0, 0)
    find_and_click_image(PRIMIS, 0, 0)
    down_command(3)
    find_and_click_image("target/communications.png", 0, 0)
    find_and_click_image("target/add.png", 0, 0)


def opt_out_form():
    global full_date
    find_and_click_image("target/solicit_code.png", 0, 0)
    keyboard.write("Imprimis")
    find_and_click_image("target/imprimis_three.png", 0, 0)
    find_and_click_image("target/wait_for_load_opt_out.png", 0, 0)
    find_and_click_image("target/prefernce_tab_down.png", 0, 0)
    find_and_click_image("target/opt_out.png", 0, 0)
    pyautogui.press("tab")
    keyboard.write(full_date)
    find_and_click_image("target/imprintis_source.png", 0, 0)
    keyboard.write("Deceased")
    find_and_click_image("target/double_deceased.png", 0, 0)
    pyautogui.press("enter")


def get_to_mark_deceased():
    find_and_click_image("target/personal_info.png", 0, 0)
    find_and_click_image("target/marked_deceased.png", 0, 0)


def interactions_num_finder():
    while True:
        pretext = "Interactions: "
        try:
            text = extract_text_from_coordinates(420, 1350, 620, 1400)
            if pretext in text:
                # Extract the number following "Interactions:"
                num_index = text.index(pretext) + len(pretext)
                num_text = text[num_index:].strip()
                num = int(extract_digits_from_text(num_text))
                break
            else:
                time.sleep(DELAY)
                continue
        except ValueError:
            time.sleep(DELAY)
            continue
    return num


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


def end_time_recording(start_time):
    end_time = time.time()
    duration = end_time - start_time
    log_file = "program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def main():
    global initials, DELAY, CRM
    input_str = pyautogui.prompt(
        text="Enter Initials and screen , -1 to quit",
        title="Enter Initials and screen , -1 to quit",
        default="DE, 1440, 900",
    )
    initials, x_scale, y_scale = input_str.strip().split(",")
    x_scale = int(x_scale.strip()) / 1440
    y_scale = int(y_scale.strip()) / 900

    find_and_click_image(CRM, 0, 0)
    while initials != "-1":
        start_time = time.time()

        get_to_dead_page()
        num = interactions_num_finder()
        interactions_section(num)
        deceased_form()
        move_to_communications()
        opt_out_form()

        end_time_recording(start_time)


if __name__ == "__main__":
    main()
