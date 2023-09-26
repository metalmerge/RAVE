# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime

import keyboard
import pyautogui
import pytesseract
from mac_notifications import client
from PIL import ImageGrab

# Interactions: 2 = 79.14 bot; 75.66 no copy pasting, experienced, fast as possible human
# Interactions: 1 = 60.42 bot; 51.08 no copy pasting, experienced, fast as possible human

# TODO get ride of needing biasX and biasY, fix extract_text_from_coordinates hard coded coordinates
# text_comment scanner did not work
# make notifcation for mac and windows
# reform num > 3
# get sound for notifications
# up and down commands to relate to screen size
# add x_scale and y_scale to all functions

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
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 1800


def find_and_click_image(image_filename, biasx, biasy):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY
    box = None
    attempts = 0
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=0.9,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                cutOffBottomY * 2,  # theocratically this works
            ),
        )
        time.sleep(DELAY)
        print("Searching for image: " + image_filename)
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            client.create_notification(
                title="Error",
                subtitle="Could not find image",
            )
            break

    x, y, width, height = box
    x = box.left / 2 + width / 4 + biasx
    y = box.top / 2 + height / 4 + biasy
    if (
        image_filename != PRIMIS
        and image_filename != "target/receives_imprimis.png"
        and image_filename != "target/wait_for_load_opt_out.png"
    ):
        pyautogui.moveTo(x, y)
        pyautogui.click()


def cord_click(cords):
    pyautogui.moveTo(cords[0], cords[1])
    pyautogui.click()


def up_command(num):
    for _ in range(0, num):
        pyautogui.press("up")


def tab_command(num):
    for _ in range(0, num):
        pyautogui.press("tab")


def down_command(num):
    for _ in range(0, num):
        pyautogui.press("down")


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


def is_text_empty(text):
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False


def get_to_dead_page():
    find_and_click_image("target/constituents.png", 0, 0)
    find_and_click_image("target/updates.png", 0, 0)
    find_and_click_image("target/name.png", 0, 25)


def confirm():
    global noted_date, initials, full_date

    find_and_click_image("target/tab_down_complete.png", 0, 0)
    find_and_click_image("target/completed_form.png", 0, 0)
    tab_command(7)
    keyboard.write(full_date)
    found_text = extract_text_from_coordinates(750, 1050, 2100, 1300)
    if (
        extract_digits_from_text(found_text) != ""
        or "year" in found_text
        or "month" in found_text
        or "January" in found_text
        or "February" in found_text
        or "March" in found_text
        or "April" in found_text
        or "May" in found_text
        or "June" in found_text
        or "July" in found_text
        or "August" in found_text
        or "September" in found_text
        or "October" in found_text
        or "November" in found_text
        or "December" in found_text
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
    global initials, CRM_cords
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
        cord_click(CRM_cords)

    return end


def click_on_top_interaction(num):
    find_and_click_image("target/status_alone.png", 0, (num * 30))
    find_and_click_image("target/edit_interaction.png", 0, 0)


def interactions_section(num):
    global PRIMIS
    OWNER = "target/wait_for_owner.png"
    find_and_click_image("target/interactions.png", 0, 0)
    down_command(num + 8)
    find_and_click_image(PRIMIS, 0, 0)
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
            cord_click(CRM_cords)
            if decline(num) == DEFAULT_PROMPT:
                duplicates = False
    up_command(num * 3)
    get_to_mark_deceased()


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
    # print(extracted_text.strip())
    return extracted_text.strip()


def move_to_communications():
    global PRIMIS
    find_and_click_image("target/constitute.png", 0, 0)
    # find_and_click_image(PRIMIS, 0, 0)
    down_command(5)
    find_and_click_image(PRIMIS, 0, 0)
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
    find_and_click_image(PRIMIS, 0, 0)
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
            continue
    return num


def end_time_recording(start_time):
    end_time = time.time()
    duration = end_time - start_time
    log_file = "program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    # find the top y coordinate of the image on the screen
    global DELAY, MAX_ATTEMPTS, x_scale, y_scale
    box = None
    attempts = 0
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=0.9,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(DELAY)
        print("Searching for image: " + image_filename)
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            client.create_notification(
                title="Error",
                subtitle="Could not find image",
            )
            break

    x, y, width, height = box
    image_cords_x = box.left / 2 + width / 4
    image_cords_y = box.top / 2 + height / 4

    return round(y / 2), (image_cords_x, image_cords_y)


def main():
    global initials, DELAY, CRM, cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY
    input_str = pyautogui.prompt(
        text="Enter Initials and screen , -1 to quit",
        title="Enter Initials and screen , -1 to quit",
        default="DE, 1440, 900",
    )
    initials, x_scale, y_scale = input_str.strip().split(",")
    cutOffBottomY = x_scale
    x_scale = int(x_scale.strip()) / 1440
    y_scale = int(y_scale.strip()) / 900
    cutOffTopY, CRM_cords = cutoff_section_of_screen("target/blackbaud_CRM.png")
    cutOffBottomY, _ = cutoff_section_of_screen("target/chrome.png")
    cord_click(CRM_cords)

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
