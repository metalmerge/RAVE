# @Dimitry Ermakov
# @09/09/2023
import re
import time
from datetime import datetime
import keyboard
import pyautogui
import pytesseract

DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
pyautogui.FAILSAFE = True
DELAY = 0.125
pyautogui.PAUSE = DELAY

current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")
full_date = current_date.strftime("%-m/%-d/%Y")


def find_and_click_image(image_filename, biasx, biasy):
    try:
        box = None
        x_scale = 1440 / 2880
        y_scale = 900 / 1800
        while box is None:
            box = pyautogui.locateOnScreen(image_filename, confidence=0.9)
            time.sleep(DELAY)
            print("Searching for image: " + image_filename)

        x, y, width, height = box

        # screenshot = pyautogui.screenshot()
        # found_image_screenshot = screenshot.crop((x, y, x + width, y + height))
        # found_image_screenshot.show()

        x = box.left * x_scale
        y = box.top * y_scale

        cord_click(x + width / 4 + biasx, y + height / 4 + biasy)
        # print(x + width / 4 + biasx, y + height / 4 + biasy)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def contains_digits(text):
    pattern = r"\d"
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


def cord_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


def get_to_dead_page():
    find_and_click_image("target/constituents.png", 0, 0)
    find_and_click_image("target/updates.png", 0, 0)
    find_and_click_image("target/name.png", 0, 25)


def click_on_first_interaction():
    find_and_click_image("target/pending_alone.png", 0, 0)
    find_and_click_image("target/edit_interaction.png", 0, 0)


def is_text_empty(text):
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False


def save_and_cancel():
    find_and_click_image("target/save.png", 0, 0)  # save button
    # find_and_click_image("target/cancel.png", 0, 0)  # cancel button


def confirm():
    global noted_date, initials, full_date
    if extract_text_from_coordinates(950, 460, 1300, 540) != "Completed":
        find_and_click_image("target/tab_down_complete.png", 0, 0)
        find_and_click_image("target/completed_form.png", 0, 0)
    if extract_text_from_coordinates(1600, 640, 2000, 700) != full_date:
        find_and_click_image("target/actual_date.png", 270, 0)

        find_and_click_image("target/today.png", 0, 0)
    found_text = extract_text_from_coordinates(750, 1050, 2100, 1300)
    # print(found_text)
    if contains_digits(found_text) is True and "year" not in found_text:
        noted_date = pyautogui.prompt(text="", title="Noted Date?", default="1/")
        find_and_click_image("target/sites.png", 0, 0)

    find_and_click_image("target/comments_form.png", 0, 0)
    if is_text_empty(found_text) == False:
        pyautogui.press("enter")
        pyautogui.press("enter")
    keyboard.write("Note: Not Researched - " + initials)

    save_and_cancel()


def decline(num):
    global initials
    if extract_text_from_coordinates(950, 460, 1300, 540) != "Declined":
        find_and_click_image("target/tab_down_complete.png", 0, 0)
        find_and_click_image("target/declined.png", 0, 0)

    if extract_text_from_coordinates(1600, 640, 2000, 700) != full_date:
        find_and_click_image("target/actual_date.png", 270, 0)
        find_and_click_image("target/today.png", 0, 0)

    find_and_click_image("target/comments_form.png", 0, 0)

    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - " + initials)

    save_and_cancel()

    if num <= 3:
        return DEFAULT_PROMPT
    elif num > 3:
        end = pyautogui.prompt(
            text="", title="More duplicates?, 1 = yes, 0 = no", default=DEFAULT_PROMPT
        )
        cord_click(194, 664)  # safe corner

    return end


def deceased_form():
    global noted_date
    find_and_click_image("target/deceased_date.png", 0, 0)
    if noted_date == "1/":
        keyboard.write(formatted_date)
    elif noted_date != "1/":
        keyboard.write(noted_date)
    find_and_click_image("target/confirmation.png", 0, 0)

    find_and_click_image("target/source_tab_down.png", 0, 0)
    find_and_click_image("target/communication_from.png", 0, 0)
    save_and_cancel()


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    # textbox_image.show()
    extracted_text = pytesseract.image_to_string(textbox_image)
    # print(extracted_text.strip())
    return extracted_text.strip()


def move_to_communications():
    find_and_click_image("target/constitute.png", 0, 0)
    time.sleep(3)
    down_command(3)
    time.sleep(3)
    find_and_click_image("target/communications.png", 0, 0)
    find_and_click_image("target/add.png", 0, 0)


def opt_out_form():
    global full_date
    find_and_click_image("target/solicit_code.png", 0, 0)
    keyboard.write("Imprimis")
    find_and_click_image("target/end_date.png", 0, 0)
    find_and_click_image("target/start_date.png", 0, 0)
    keyboard.write(full_date)
    find_and_click_image("target/prefernce_tab_down.png", 0, 0)
    find_and_click_image("target/opt_out.png", 0, 0)
    find_and_click_image("target/imprintis_source.png", 0, 0)
    keyboard.write("Deceased")
    find_and_click_image("target/source_evidence.png", 0, 0)
    down_command(3)
    find_and_click_image("target/save.png", 0, 0)
    # find_and_click_image("target/cancel.png", 0, 0)  # cancel button


def down_command(num):
    for _ in range(0, num):
        pyautogui.press("down")


def get_to_mark_deceased():
    find_and_click_image("target/personal_info.png", 0, 0)
    find_and_click_image("target/marked_deceased.png", 0, 0)


def interactions_section(num):
    time.sleep(3)
    down_command(8)
    time.sleep(3)
    click_on_first_interaction()

    if num == 1:
        confirm()
        get_to_mark_deceased()

    elif num == 2:
        confirm()
        time.sleep(3)
        down_command(2)
        time.sleep(3)
        click_on_first_interaction()

        decline(num)

        get_to_mark_deceased()

    elif num == 3:
        confirm()
        click_on_first_interaction()

        decline(num)
        time.sleep(3)
        down_command(2)
        time.sleep(3)
        click_on_first_interaction()
        decline(num)

        get_to_mark_deceased()

    elif num > 3:
        confirm()

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

        get_to_mark_deceased()


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


def main():
    global initials, LAST_MOUSE_MOVE_TIME, DELAY
    initials = pyautogui.prompt(
        text="", title="Enter Initials, -1 to quit", default="DE"
    )
    cord_click(271, 173)
    while initials != "-1":
        DELAY /= 2
        print(DELAY)
        start_time = time.time()

        get_to_dead_page()

        while True:
            try:
                num = int(
                    extract_digits_from_text(
                        extract_text_from_coordinates(420, 1350, 620, 1400)
                    )
                )
                break
            except ValueError:
                time.sleep(DELAY)
                continue

        find_and_click_image("target/interactions.png", 0, 0)
        interactions_section(num)
        deceased_form()
        move_to_communications()
        opt_out_form()
        end_time = time.time()
        duration = end_time - start_time
        log_file = "program_log.txt"
        with open(log_file, "a") as f:
            f.write(f"Program execution time: {duration:.2f} seconds\n")


if __name__ == "__main__":
    main()
