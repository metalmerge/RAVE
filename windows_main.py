# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime
import pygame
import pyperclip
import keyboard
import pyautogui
import re
from date_extractor import extract_dates

from main_shared_functions import (
    extract_text_from_coordinates,
    # extract_dates,
    tab_command,
    extract_digits_from_text,
    remove_numbers_greater_than_current_year,
    remove_phone_numbers,
    remove_digits_next_to_letters,
)


x_scale = 1
y_scale = 1
COM_NUM = 1
delay = 0.04
deincrement = 0.27
confidence = 0.7
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900
pyautogui.FAILSAFE = True
pyautogui.PAUSE = delay
DEFAULT_PROMPT = "0"
noted_date = "1/"
IMPRIMIS = "windowsTarget/receives_imprimis.png"
LOAD_OWNER_WAIT = "windowsTarget/wait_for_load_owner.png"
PRIMARY_EMAIL = "windowsTarget/primary_email.png"
CURRENT_DATE = datetime.now()
formatted_month = str(CURRENT_DATE.month)
formatted_year = str(CURRENT_DATE.year)
formatted_day = str(CURRENT_DATE.day)
FORMATTED_DATE = f"{formatted_month}/{formatted_year}"
FULL_DATE = f"{formatted_month}/{formatted_day}/{formatted_year}"


def find_and_click_image(image_filename, biasx=0, biasy=0, up_or_down=None):
    global cutOffTopY, delay, x_scale, y_scale, cutOffBottomY, confidence, PRIMARY_EMAIL, IMPRIMIS, LOAD_OWNER_WAIT
    box = None
    attempts = 0
    if (
        image_filename == "windowsTarget/source_file_tab_down.png"
        or image_filename == "windowsTarget/status_alone.png"
    ):
        confidence = 0.8
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
            factor = 14 if up_or_down == "up" else -14
            pyautogui.scroll(factor)
            time.sleep(delay * 2)
        attempts += 1
        if attempts > 25:
            play_sound("alert_notification.mp3")
            time.sleep(2)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy
    if image_filename not in [
        IMPRIMIS,
        PRIMARY_EMAIL,
        LOAD_OWNER_WAIT,
        "windowsTarget/personal_info_wait.png",
        "windowsTarget/source_wait.png",
        "windowsTarget/preference.png",
    ]:
        pyautogui.moveTo(x, y)
        pyautogui.click()


def month_year_only(input_text):
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
    month_year_pattern = r"\b([A-Za-z]+)[ /-](\d{4})\b"
    month_year_match = re.search(month_year_pattern, input_text)
    if month_year_match:
        month = months.get(month_year_match.group(1))
        year = month_year_match.group(2)
        if month:
            return f"{month}/{year}"
    return None


def formatted_extract_date(input_text):
    dates = extract_dates(input_text)
    print(f"{dates}:{input_text}")
    if dates:
        month_year_result = month_year_only(input_text)
        if month_year_result is not None:
            return month_year_result
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
    try:
        date = dates[0]
        month = date.month
        year = date.year
        return f"{month}/{year}"
    except IndexError:
        print("Fail")
        return "1/"


def get_to_dead_page():
    global COM_NUM, delay

    find_and_click_image("windowsTarget/constituents.png")
    find_and_click_image("windowsTarget/updates.png")
    if COM_NUM == 2:
        find_and_click_image("windowsTarget/third_page.png")
        time.sleep(5)
    if COM_NUM == 3:
        find_and_click_image("windowsTarget/fifth_page.png")
        time.sleep(5)
    find_and_click_image("windowsTarget/name.png", 0, round(25 * y_scale))


def interactions_num_finder():
    global delay
    while True:
        pretext = "Interactions: "
        try:
            text = extract_text_from_coordinates(
                1196,
                491,  # 478,
                1281,
                517,  # 499,
            )
            if pretext in text:
                num_index = text.index(pretext) + len(pretext)
                num_text = text[num_index:].strip()
                number_of_interactions = int(extract_digits_from_text(num_text))
                break
            else:
                time.sleep(delay)
                continue
        except ValueError:
            continue
    return number_of_interactions


def click_on_top_interaction(number_of_interactions):
    global IMPRIMIS, PRIMARY_EMAIL, LOAD_OWNER_WAIT, deincrement
    if number_of_interactions == 1:
        time.sleep(0.99 - deincrement)
        find_and_click_image(LOAD_OWNER_WAIT)
        find_and_click_image(IMPRIMIS)
        # time.sleep(0.25 - deincrement)
    find_and_click_image(
        "windowsTarget/status_alone.png",
        40,
        round(number_of_interactions * 25),
        "down",
    )
    find_and_click_image("windowsTarget/edit_interaction.png", 0, 0, "down")


def interactions_section(number_of_interactions, initials):
    global LOAD_OWNER_WAIT, PRIMARY_EMAIL
    find_and_click_image("windowsTarget/interactions.png")
    click_on_top_interaction(1)
    process_application(True, initials)
    if number_of_interactions > 1:
        for i in range(2, number_of_interactions + 1):
            find_and_click_image(IMPRIMIS)
            find_and_click_image(PRIMARY_EMAIL)
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            # find_and_click_image(LOAD_OWNER_WAIT)
            process_application(False, initials)
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "up")
    find_and_click_image("windowsTarget/personal_info.png")
    find_and_click_image("windowsTarget/personal_info_wait.png")  # , 0, 0, "down"
    find_and_click_image("windowsTarget/marked_deceased.png")


def process_application(is_confirmed=True, initials="DE"):
    global noted_date, FULL_DATE, deincrement
    if is_confirmed:
        find_and_click_image("windowsTarget/tab_down_complete.png")
        find_and_click_image("windowsTarget/completed_form.png")
        find_and_click_image("windowsTarget/wait_for_complete.png")
    else:
        find_and_click_image("windowsTarget/tab_down_complete.png")
        find_and_click_image("windowsTarget/declined.png")
        find_and_click_image("windowsTarget/wait_for_declined.png")
    time.sleep(0.99 - deincrement)
    find_and_click_image("windowsTarget/actual_date.png")
    keyboard.press_and_release("ctrl+a")
    keyboard.write(FULL_DATE)
    tab_command(3)
    pyperclip.copy("")
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.5 - deincrement)
    found_text = pyperclip.paste()
    found_text = remove_phone_numbers(found_text)
    found_text = remove_numbers_greater_than_current_year(found_text)
    found_text = remove_digits_next_to_letters(found_text)
    specific_words = [
        "year",
        "month",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    if any(
        extract_digits_from_text(found_text) != "" or word in found_text
        for word in specific_words
    ):
        play_sound("alert_notification.mp3")
        noted_date = pyautogui.prompt(
            text="", title="Noted Date?", default=formatted_extract_date(found_text)
        )
        find_and_click_image("windowsTarget/sites.png")
        tab_command(2)
    if found_text != "":
        pyautogui.press("down")
        pyautogui.press("enter")
        pyautogui.press("enter")

    if is_confirmed:
        keyboard.write("Note: Not Researched - " + initials)
    else:
        keyboard.write("Note: Duplicate - " + initials)

    tab_command(2)
    pyautogui.press("enter")


def play_sound(music_file):
    pygame.init()
    sound = pygame.mixer.Sound(music_file)
    sound.play()
    sound.set_volume(1)
    pygame.mixer.music.stop()


def deceased_form():
    global noted_date, FORMATTED_DATE
    find_and_click_image("windowsTarget/source_tab_down.png")
    find_and_click_image("windowsTarget/communication_from.png")
    find_and_click_image("windowsTarget/deceased_date.png")
    if noted_date == "1/":
        keyboard.write(FORMATTED_DATE)
    elif noted_date != "1/":
        keyboard.write(noted_date)
        noted_date = "1/"
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("space")


def move_to_communications():
    global IMPRIMIS, deincrement
    find_and_click_image("windowsTarget/constitute.png")
    find_and_click_image(IMPRIMIS)
    # time.sleep(0.25 - deincrement)
    # find_and_click_image("windowsTarget/communications.png")
    find_and_click_image("windowsTarget/preference.png")
    find_and_click_image("windowsTarget/add.png")


def opt_out_form():
    global FULL_DATE
    time.sleep(0.01)
    find_and_click_image("windowsTarget/solicit_code.png")
    keyboard.write("Imprimis")
    find_and_click_image("windowsTarget/imprimis_three.png")
    find_and_click_image("windowsTarget/source_wait.png")
    find_and_click_image("windowsTarget/opt_out_tab_down.png")
    find_and_click_image("windowsTarget/opt_out.png")
    pyautogui.press("tab")
    keyboard.write(FULL_DATE)
    tab_command(3)
    keyboard.write("Deceased")
    find_and_click_image("windowsTarget/double_deceased.png")
    pyautogui.press("enter")


def end_time_recording(start_time):
    end_time = time.time()
    duration = end_time - start_time
    log_file = "time_logs/windows_program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    global delay, x_scale, y_scale, confidence
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
    global cutOffTopY, cutOffBottomY, x_scale, y_scale, CRM_cords, COM_NUM, delay, deincrement, PRIMARY_EMAIL
    input_str = pyautogui.prompt(
        text="Enter Initials, which computer number this is, and delay time; -1 to quit",
        title="Enter Initials, which computer number this is, and delay time; -1 to quit",
        default="DE, 1, 0.04, 0.27",
    )
    initials, computer_number, delay, deincrement = input_str.strip().split(",")
    COM_NUM = int(computer_number)
    delay = float(delay)
    deincrement = float(deincrement)
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while initials != "-1":
        start_time = time.time()
        get_to_dead_page()
        number_of_interactions = interactions_num_finder()
        interactions_section(number_of_interactions, initials)
        deceased_form()
        move_to_communications()
        opt_out_form()
        end_time_recording(start_time)
        find_and_click_image(PRIMARY_EMAIL)
        # print(f"Deincrement: {deincrement}")
        # deincrement += 0.01


if __name__ == "__main__":
    main()
