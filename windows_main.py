# @Dimitry Ermakov
# @09/23/2023
import schedule
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

# TODO
# Potential improvements:
#   - Find a better way to know the number of interactions than using extract_text_from_coordinates
#   - Use mss to take screenshots instead of pyautogui

# original_x_scale = 1440 / 2880
# original_y_scale = 900 / 1800

x_scale = 1
y_scale = 1
COM_NUM = 1
delay = 0.05
confidence = 0.7
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900
pyautogui.FAILSAFE = True
pyautogui.PAUSE = delay
DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
IMPRIMIS = "windowsTarget/receives_imprimis.png"
EDUCATION = "windowsTarget/education.png"
LOAD_OPT_OUT_WAIT = "windowsTarget/wait_for_load_opt_out.png"
LOAD_OWNER_WAIT = "windowsTarget/wait_for_load_owner.png"
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

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy
    if image_filename not in [
        IMPRIMIS,
        EDUCATION,
        PRIMARY_EMAIL,
        LOAD_OPT_OUT_WAIT,
        LOAD_OWNER_WAIT,
        "windowsTarget/personal_info_wait.png",
        "windowsTarget/source_wait.png",
        "windowsTarget/preference.png",
    ]:
        cord_click((x, y))


def get_to_dead_page():
    global COM_NUM, delay

    find_and_click_image("windowsTarget/constituents.png")
    # time.sleep(0.05 + delay)
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
                478,  # 491,
                1281,
                499,  # 517,
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
    global IMPRIMIS, PRIMARY_EMAIL, LOAD_OWNER_WAIT
    if number_of_interactions == 1:
        time.sleep(1)
        find_and_click_image(LOAD_OWNER_WAIT)
        find_and_click_image(IMPRIMIS)
        time.sleep(0.25)
    find_and_click_image(
        "windowsTarget/status_alone.png",
        40,
        round(number_of_interactions * 25),
        "down",
    )
    find_and_click_image("windowsTarget/edit_interaction.png", 0, 0, "down")


def interactions_section(number_of_interactions):
    global LOAD_OWNER_WAIT, PRIMARY_EMAIL
    find_and_click_image("windowsTarget/interactions.png")
    click_on_top_interaction(1)
    process_application()
    if number_of_interactions > 1:
        for i in range(2, number_of_interactions + 1):
            find_and_click_image(IMPRIMIS)
            find_and_click_image(PRIMARY_EMAIL)
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            # find_and_click_image(LOAD_OWNER_WAIT)
            process_application(False)
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "up")
    find_and_click_image("windowsTarget/personal_info.png")
    find_and_click_image("windowsTarget/personal_info_wait.png")  # , 0, 0, "down"
    find_and_click_image("windowsTarget/marked_deceased.png")


def process_application(is_confirmed=True):
    global initials, noted_date, FULL_DATE
    if is_confirmed:
        find_and_click_image("windowsTarget/tab_down_complete.png")
        find_and_click_image("windowsTarget/completed_form.png")
        find_and_click_image("windowsTarget/wait_for_complete.png")
    else:
        find_and_click_image("windowsTarget/tab_down_complete.png")
        find_and_click_image("windowsTarget/declined.png")
        find_and_click_image("windowsTarget/wait_for_declined.png")
    time.sleep(1)
    find_and_click_image("windowsTarget/actual_date.png")
    keyboard.press_and_release("ctrl+a")
    keyboard.write(FULL_DATE)
    tab_command(3)
    pyperclip.copy("")
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.5)
    found_text = pyperclip.paste()
    found_text = remove_phone_numbers(found_text)
    found_text = remove_numbers_greater_than_current_year(found_text)
    found_text = remove_digits_next_to_letters(found_text)
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
        play_sound("alert_notification.mp3")
        noted_date = pyautogui.prompt(
            text="", title="Noted Date?", default=extract_date(found_text)
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
    find_and_click_image("windowsTarget/deceased_date.png")
    if noted_date == "1/":
        keyboard.write(FORMATTED_DATE)
    elif noted_date != "1/":
        keyboard.write(noted_date)
        noted_date = "1/"
    find_and_click_image("windowsTarget/source_tab_down.png")
    find_and_click_image("windowsTarget/communication_from.png")
    pyautogui.press("enter")


def move_to_communications():
    global IMPRIMIS
    find_and_click_image("windowsTarget/constitute.png")
    find_and_click_image(IMPRIMIS)
    time.sleep(0.25)
    # find_and_click_image("windowsTarget/communications.png")
    find_and_click_image("windowsTarget/preference.png")
    find_and_click_image("windowsTarget/add.png")


def opt_out_form():
    global FULL_DATE
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
        text="Enter Initials, which computer number this is, and delay time -1 to quit",
        title="Enter Initials, which computer number this is, and delay time -1 to quit",
        default="DE, 1, 0.04",
    )
    initials, computer_number, delay = input_str.strip().split(",")
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    delay = float(delay.strip())
    COM_NUM = int(computer_number.strip())
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while initials != "-1":
        start_time = time.time()
        get_to_dead_page()
        number_of_interactions = interactions_num_finder()
        interactions_section(number_of_interactions)
        deceased_form()
        move_to_communications()
        opt_out_form()
        end_time_recording(start_time)
        find_and_click_image(PRIMARY_EMAIL)
        schedule.run_pending()


schedule.every().day.at("2:57").do(play_sound("quittingTime.mp3"))

if __name__ == "__main__":
    main()
