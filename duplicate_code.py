# @Dimitry Ermakov
# @2/24/2024
# CRUD = Create, Read, Update, and Delete
import time
import keyboard
import pyautogui
from pyautogui import ImageNotFoundException
from datetime import datetime
from main_shared_functions import (
    cord_click,
    tab_command,
    extract_text_from_coordinates,
    extract_digits_from_text,
)
from windows_main import play_sound
import sys

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


def find_and_click_image(
    image_filename, biasx=0, biasy=0, up_or_down=None, max_attempts=50
):
    global cutOffTopY, delay, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, confidence
    box = None
    attempts = 0
    if image_filename == "images_duplicate/comment.png":
        confidence = 0.9
    while box is None and attempts < max_attempts:
        try:
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
        except ImageNotFoundException:
            if attempts > max_attempts:
                play_sound("audio/alert_notification.mp3")
                time.sleep(2)
            attempts += 1
            if box is None and up_or_down and up_or_down != "NULL":
                factor = 200 if up_or_down == "up" else -200
                pyautogui.scroll(factor)
                time.sleep(delay * 2)
            continue
        time.sleep(delay * 5)
        print(image_filename)

    if box is not None:
        x, y, width, height = box
        x = box.left + width / 2 + biasx
        y = box.top + height / 2 + biasy
        if up_or_down != "NULL":
            cord_click((x, y))
        return x, y
    else:
        return None, None


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


def get_screen_dimensions():
    screen_width, screen_height = pyautogui.size()
    return screen_width / 1440, screen_height / 900, screen_height


def process_answer(answer, start_date, end_date):
    print(answer)
    if answer == "q":
        find_and_click_image("images_duplicate/comment.png", 0, 25)
        find_and_click_image("images_duplicate/save.png")
        sys.exit()
    elif answer == "i":
        opt_form(start_date, end_date, True)
    elif answer == "o":
        opt_form(start_date, end_date, False)
    # elif answer == "c":
    #     no_contact_form(start_date, end_date)
    # elif answer == "ndo":
    #     ndo_form(start_date, end_date)
    elif answer == "dnc":
        delete_specifc_form("mergeConflictImages/noContact.png")
    elif answer == "dnn":
        delete_specifc_form("mergeConflictImages/noNDO.png")
    elif answer == "dva":
        pyautogui.press("down", presses=2)
        time.sleep(1)
        delete_specifc_form("images_duplicate/noValidAddress.png")
    elif answer == "dni":
        delete_specifc_form("images_duplicate/no_imprintis.png")
    elif answer.isdigit():
        if int(answer) >= 3:
            pyautogui.press("down", presses=2)
            time.sleep(1)
        delete_specifc_form(
            "images_duplicate/review_down.png", 0, (80 + ((int(answer) - 1) * 25))
        )


def opt_form(start_date, end_date, opt_in):
    find_and_click_image("images_duplicate/target_select.png", 0, 40)
    if opt_in:
        find_and_click_image("images_duplicate/opt_in_button.png")
    else:
        find_and_click_image("images_duplicate/opt_in_button.png", 100)

    time.sleep(3)
    pyautogui.press("tab", presses=2)

    if start_date is not None:
        keyboard.write(start_date)
    pyautogui.press("tab")
    if end_date is not None:
        keyboard.write(end_date)
    pyautogui.press("tab", presses=7)  # TODO test
    pyautogui.press("enter")
    # time.sleep(3)
    # find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL")
    # pyautogui.press("down", presses=12)
    # time.sleep(1)


def no_contact_form(start_date, end_date):
    find_and_click_image("windowsTarget/add.png", 0, 0, "down")
    time.sleep(0.02)
    find_and_click_image("windowsTarget/solicit_code.png", 0, 0, None)
    keyboard.write("No Contact")
    find_and_click_image("mergeConflictImages/no_contact_menu.png", 0, 0, None)
    pyautogui.press("tab")
    if start_date is not None:
        keyboard.write(start_date)
    tab_command(1)
    if end_date is not None:
        keyboard.write(end_date)
    tab_command(2)
    pyautogui.press("enter")
    time.sleep(3)
    # find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL")
    # pyautogui.press("down", presses=12)


def ndo_form(start_date, end_date):
    find_and_click_image("windowsTarget/add.png", 0, 0, "down")
    time.sleep(0.02)
    find_and_click_image("windowsTarget/solicit_code.png", 0, 0, None)
    keyboard.write("No NDO Direct Mail Fundraising")
    find_and_click_image("mergeConflictImages/noNDOForm.png", 0, 0, None)
    pyautogui.press("tab")
    if start_date is not None:
        keyboard.write(start_date)
    tab_command(1)
    if end_date is not None:
        keyboard.write(end_date)
    tab_command(2)
    pyautogui.press("enter")
    time.sleep(3)
    # find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL")
    # pyautogui.press("down", presses=12)


def delete_specifc_form(image, biasx=30, biasy=0):
    while True:
        x, y = find_and_click_image(image, biasx, biasy)
        if x == None and y == None:
            break
        find_and_click_image("mergeConflictImages/delete.png")
        find_and_click_image("images_duplicate/yes.png")
        if image == "images_duplicate/review_down.png":
            break
        time.sleep(3)
        # find_and_click_image(
        #     PRIMARY_EMAIL,
        #     0,
        #     0,
        #     "NULL",
        # )
        # pyautogui.press("down", presses=12)
        # time.sleep(1)


def allowed_constituencies():
    x, y = find_and_click_image("mergeConflictImages/constitencies.png", 0, 0, "NULL")
    print(x, y)
    amount = ""
    attempts = 0
    while amount == "" and attempts < 30:
        amount = extract_text_from_coordinates(x + 45, y - 10, x + 450, y + 10)  # TODO
        print(f"Text: {amount}")
        attempts += 1
    listAmount = amount.split(" ")
    text = [
        "Trustee",
        "Prospect",
        " Prospect",
        "prospect",
        "Student",
        "Staff",
        # "Planned Giver",
        # "Parent",
        # "Major Donor",
        # "Grandparent",
        "Faculty",
        "Academy Student",
        # "Alumnus - Graduated",
        # "Alumnus - Not Graduated",
        # "Donor",
    ]
    for x in listAmount:
        if x in text:
            return -1
    return 0


def merge_request():
    find_and_click_image("images_duplicate/comment.png", 0, 25)
    find_and_click_image("images_duplicate/save.png")
    time.sleep(1)
    find_and_click_image("images_duplicate/return.png")


def main():
    global delay, x_scale, y_scale, cutOffBottomY, cutOffTopY, CRM_cords
    x_scale, y_scale, cutOffBottomY = get_screen_dimensions()
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while True:
        find_and_click_image("windowsTarget/updates.png")
        find_and_click_image("images_duplicate/target_lookup_id.png", -30, 25)
        if allowed_constituencies() != -1:
            pyautogui.press("down", presses=5)
            time.sleep(1)
            find_and_click_image("images_duplicate/target_select.png", 0, 50)
            time.sleep(1)
            find_and_click_image("images_duplicate/source_target.png", 0, 50)
            add = pyautogui.prompt(
                text="Addresses Correct?",
                title="Addresses",
                default="y",
            )
            if add != "y":
                continue
            find_and_click_image("images_duplicate/target_select.png", 0, 50)
            time.sleep(1)
            find_and_click_image("images_duplicate/source_target.png", 0, 50)
            answer = None
            # x1, y1 = find_and_click_image(
            #     "images_duplicate/start_date.png", 0, 0, "NULL"
            # )
            # guess = extract_text_from_coordinates(
            #     x1 - 40, y1 + 45, x1 + 40, y1 + 68
            # )  # TODO
            # x2, y2 = find_and_click_image("images_duplicate/end_date.png", 0, 0, "NULL")
            # guessTwo = extract_text_from_coordinates(
            #     x2 - 40, y2 + 45, x2 + 40, y2 + 68
            # )  # TODO
            # defaultGuess = f"i {guess}"
            defaultGuess = f"3"
            # if guessTwo != "":
            #     defaultGuess = f"i {guess} {guessTwo}"

            # delete_specifc_form("images_duplicate/noValidAddress.png")
            # delete_specifc_form("images_duplicate/no_current.png")

            while True:
                response = pyautogui.prompt(
                    text="i = opt in; o = opt out; dnc = delete no contact; dnn = delete NDO; dva = delete no valid address; dni = delete no imprintis; q = stop; e",
                    title="Command",
                    default=defaultGuess,
                )
                commands = response.split(",")

                for index, command in enumerate(commands):
                    parts = command.strip().split(" ")
                    answer = parts[0] if len(parts) > 0 else None
                    start_date = parts[1] if len(parts) > 1 else None
                    end_date = parts[2] if len(parts) > 2 else None
                    process_answer(answer, start_date, end_date)

                    if index != len(commands) - 1:
                        time.sleep(3)
                if commands[-1].strip().split(" ")[0] != "e":
                    defaultGuess = "e"
                    continue
                if commands[-1].strip().split(" ")[0] == "e":
                    merge_request()
                break
        else:
            pyautogui.alert(
                text="This constituent is not allowed to be solicited",
                title="Error",
                button="OK",
            )
            merge_request()


if __name__ == "__main__":
    main()
