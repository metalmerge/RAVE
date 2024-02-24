# @Dimitry Ermakov
# @12/06/2023
import time
import pyperclip
import keyboard
import pyautogui
import os
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
from tqdm import tqdm

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
namesOne = None
namesTwo = None


def find_and_click_image(
    image_filename, biasx=0, biasy=0, up_or_down=None, max_attempts=20
):
    global cutOffTopY, delay, x_scale, y_scale, cutOffBottomY, confidence, PRIMARY_EMAIL, IMPRIMIS, LOAD_OWNER_WAIT, PREVIOUS_ClICK, PRECIOUS_BIASX, PRECIOUS_BIASY
    box = None
    attempts = 0
    print(image_filename)
    if (
        image_filename == "windowsTarget/source_file_tab_down.png"
        or image_filename == "windowsTarget/status_alone.png"
    ):
        confidence = 0.8

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=max_attempts, desc="Attempts", position=0)

    while box is None:
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
            attempts += 1
            progress_bar.update(1)  # Update progress bar
            if attempts >= max_attempts:
                play_sound("audio/alert_notification.mp3")
                attempts = 0
                if PREVIOUS_ClICK in [
                    "windowsTarget/solicit_code.png",
                    "windowsTarget/actual_date.png",
                ]:
                    if PREVIOUS_ClICK == "windowsTarget/solicit_code.png":
                        find_and_click_image(
                            PREVIOUS_ClICK, PRECIOUS_BIASX, PRECIOUS_BIASY, up_or_down
                        )
                        time.sleep(0.25)
                        keyboard.write("Imprimis")
                    elif PREVIOUS_ClICK == "windowsTarget/actual_date.png":
                        # time.sleep(2)
                        find_and_click_image(
                            PREVIOUS_ClICK, PRECIOUS_BIASX, PRECIOUS_BIASY, up_or_down
                        )
                        time.sleep(0.2)
                        keyboard.press_and_release("ctrl+a")
                        keyboard.write(FULL_DATE)
                        pyautogui.press("tab", presses=5)
                        pyautogui.press("enter")
                else:
                    find_and_click_image(
                        PREVIOUS_ClICK, PRECIOUS_BIASX, PRECIOUS_BIASY, up_or_down
                    )

            if box is None and up_or_down:
                factor = 14 if up_or_down == "up" else -14
                pyautogui.scroll(factor)
            time.sleep(0.5)
            continue
        time.sleep(delay * 5)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy
    PREVIOUS_ClICK = image_filename
    PRECIOUS_BIASX = biasx
    PRECIOUS_BIASY = biasy
    if image_filename not in [
        IMPRIMIS,
        PRIMARY_EMAIL,
        LOAD_OWNER_WAIT,
        "windowsTarget/personal_info_wait.png",
        "windowsTarget/source_wait.png",
        "windowsTarget/preference.png",
        "windowsTarget/interactionsExtract.png",
        "windowsTarget/interactionsBASED.png",
    ]:
        pyautogui.click(x, y)
    progress_bar.close()  # Close progress bar after completion
    return x, y


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


def convert_date(date_str):
    if date_str is None:
        return None
    # Convert the date string to a datetime object
    # date = datetime.strptime(date_str, "%m%d%Y")
    # Convert the date back to a string in the desired format
    string = date_str
    if len(string) == 6:
        print(string[:2] + "/" + string[2:4] + "/20" + string[4:])
        return string[:2] + "/" + string[2:4] + "/20" + string[4:]
    print(string[:2] + "/" + string[2] + string[3] + "/" + string[4:])
    return string[:2] + "/" + string[2] + string[3] + "/" + string[4:]
    # TODO No NDO Direct Mail Fundraising
    # Write all commands in one prompt
    # Refactor code
    # if the last command is not e then prompt
    # Size(width=1920, height=1080)
    # find & get all details and then try to make timeline
    # -710
    # 27 height whole, so 13 up and down
    # opt = -645 to -580
    # start = -540 to -360
    # e = -348 to -254


def get_screen_dimensions():
    screen_width, screen_height = pyautogui.size()
    return screen_width / 1440, screen_height / 900, screen_height


def process_lookup_id(lookup_id, opt_in=True):
    find_and_click_image("windowsTarget/constituteSearch.png", 0, 0, None, opt_in)
    time.sleep(1)
    find_and_click_image("mergeConflictImages/lookupID.png")
    time.sleep(0.25)
    keyboard.press_and_release("ctrl+a")
    time.sleep(0.25)
    keyboard.write(str(lookup_id))
    pyautogui.press("enter")
    find_and_click_image("windowsTarget/cityStateZIP.png", 0, 5)
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", opt_in)
    # x1, y1 = find_and_click_image(
    #     "mergeConflictImages/donor.png", 0, 0, "NULL", opt_in, 3
    # )
    x2, y2 = find_and_click_image(
        "mergeConflictImages/constitencies.png", 0, 0, "NULL", opt_in, 5
    )
    print(x2, y2)
    if x2 == None:
        return None, None
    x = int(x2)
    y = int(y2)
    amount = None
    while not amount:
        amount = extract_text_from_coordinates(x + 45, y - 10, x + 450, y + 10)
        print(f"Text: {amount}")

    text = [
        "Trustee",
        "Student",
        "Staff",
        "Planned Giver",
        "Parent",
        "Major Donor",
        "Grandparent",
        "Faculty",
        "Academy Student",
        "Alumnus - Graduated",
        "Alumnus - Not Graduated",
        "Donor",
    ]
    for word in text:
        if word in amount:
            return word, 1

    # other = pyautogui.prompt(
    #         text="Trustee, Student, Staff, Planned Giver, Parent, Major Donor, Grandparent, Faculty, Academy Student, Alumnus - Graduated, Alumnus - Not Graduated",
    #         title="Other?",
    #         default="No",
    #     )
    # if other != "No":
    #     return 1, 1
    return None, None


def write_to_file(filename, content):
    # if not os.path.exists(filename):
    #     print("No exist")
    #     with open("input.txt", "w") as f:
    #         f.write("")
    # pyautogui.alert(
    #     text="Please enter LookUp IDs in the input.txt file",
    #     title="LookUp IDs",
    # )
    with open(filename, "a") as f:
        f.write(content)


def process_answer(answer, start_date, end_date, saveOne, saveTwo):
    if answer == "n":
        write_to_file("lookup_ids.txt", f"{saveOne} XXX\n{saveTwo} XXX\n")
    elif answer == "q":
        delete_form()
        write_to_file("lookup_ids.txt", f"{saveOne}\n{saveTwo}\n")
        sys.exit()
    elif answer == "i":
        opt_form(start_date, end_date, True)
    elif answer == "o":
        opt_form(start_date, end_date, False)
    elif answer == "c":
        no_contact_form(start_date, end_date)
    elif answer == "ndo":
        ndo_form(start_date, end_date)
    elif answer == "dnc":
        find_and_click_image("mergeConflictImages/noContact.png", 0, 0, None, False)
        time.sleep(1)
        find_and_click_image("mergeConflictImages/delete.png", 0, 0, None, False)
        find_and_click_image("mergeConflictImages/yes.png", 0, 0, None, False)
        time.sleep(1)
        find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
        # pyautogui.press("down", presses=12)
        # time.sleep(1)
    elif answer == "dnn":
        find_and_click_image("mergeConflictImages/noNDO.png", 0, 0, None, False)
        time.sleep(1)
        find_and_click_image("mergeConflictImages/delete.png", 0, 0, None, False)
        find_and_click_image("mergeConflictImages/yes.png", 0, 0, None, False)
        time.sleep(1)
        find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
        # pyautogui.press("down", presses=12)
        # time.sleep(1)


def codes_num_finder():
    x, y = find_and_click_image("mergeConflictImages/add.png", 0, 0, "NULL", True)
    print(x, y)
    x = int(x)
    y = int(y)
    amount = None
    while not amount:
        amount = extract_digits_from_text(
            extract_text_from_coordinates(x - 60, y - 20, x - 35, y + 20)
        )
        print(f"Solicit Codes: {amount}")
    return int(amount)


def opt_form(start_date, end_date, opt_in):
    find_and_click_image("windowsTarget/add.png", 0, 0, "down", False)
    time.sleep(0.02)
    find_and_click_image("windowsTarget/solicit_code.png", 0, 0, None, False)
    keyboard.write("Imprimis")
    find_and_click_image("windowsTarget/imprimis_three.png", 0, 0, None, False)
    time.sleep(0.3)
    # find_and_click_image("windowsTarget/source_wait.png", 0, 0, None, False)
    find_and_click_image("windowsTarget/opt_out_tab_down.png", 0, 0, None, False)
    if opt_in:
        find_and_click_image("mergeConflictImages/opt_in_menu.png", 0, 0, None, False)
    else:
        find_and_click_image("windowsTarget/opt_out.png", 0, 0, None, False)
    pyautogui.press("tab")
    if start_date is not None:
        keyboard.write(start_date)
    tab_command(1)
    if end_date is not None:
        keyboard.write(end_date)
    tab_command(2)
    keyboard.write("Constituent")
    find_and_click_image("mergeConflictImages/consit_menu.png")
    pyautogui.press("enter")
    time.sleep(1)
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
    # pyautogui.press("down", presses=12)
    # time.sleep(1)


def no_contact_form(start_date, end_date):
    find_and_click_image("windowsTarget/add.png", 0, 0, "down", False)
    time.sleep(0.02)
    find_and_click_image("windowsTarget/solicit_code.png", 0, 0, None, False)
    keyboard.write("No Contact")
    find_and_click_image("mergeConflictImages/no_contact_menu.png", 0, 0, None, False)
    pyautogui.press("tab")
    if start_date is not None:
        keyboard.write(start_date)
    tab_command(1)
    if end_date is not None:
        keyboard.write(end_date)
    tab_command(2)
    pyautogui.press("enter")
    time.sleep(1)
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
    # pyautogui.press("down", presses=12)


def ndo_form(start_date, end_date):
    find_and_click_image("windowsTarget/add.png", 0, 0, "down", False)
    time.sleep(0.02)
    find_and_click_image("windowsTarget/solicit_code.png", 0, 0, None, False)
    keyboard.write("No NDO Direct Mail Fundraising")
    find_and_click_image("mergeConflictImages/noNDOForm.png", 0, 0, None, False)
    pyautogui.press("tab")
    if start_date is not None:
        keyboard.write(start_date)
    tab_command(1)
    if end_date is not None:
        keyboard.write(end_date)
    tab_command(2)
    pyautogui.press("enter")
    time.sleep(1)
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
    # pyautogui.press("down", presses=12)


def delete_form(image):
    for _ in range(codes_num_finder()):
        find_and_click_image(f"mergeConflictImages/{image}.png", 0, 25, None, True)
        find_and_click_image("mergeConflictImages/delete.png", 0, 0, None, True)
        find_and_click_image("mergeConflictImages/yes.png", 0, 0, None, True)
        time.sleep(1)
        find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", True)
        # pyautogui.press("down", presses=12)
        # time.sleep(1)


def main():
    global delay, x_scale, y_scale, cutOffBottomY, cutOffTopY, CRM_cords, namesOne, namesTwo
    x_scale, y_scale, cutOffBottomY = get_screen_dimensions()
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while True:
        lookup_idOne, lookup_idTwo = get_lookup_ids()
        lookup_idOne = int(lookup_idOne)
        lookup_idTwo = int(lookup_idTwo)
        saveOne = lookup_idOne
        saveTwo = lookup_idTwo
        if lookup_idOne < lookup_idTwo:
            lookup_idOne, lookup_idTwo = lookup_idTwo, lookup_idOne
        if lookup_idOne == "-1" or lookup_idTwo == "-1":
            break
        print(f"{saveOne}\n{saveTwo}")
        pyperclip.copy(f"{saveOne}\n{saveTwo}")

        xC, yC = process_lookup_id(lookup_idOne)
        # pyautogui.press("down", presses=12)
        # time.sleep(1)
        if codes_num_finder() != 0 and xC is None and yC is None:
            xC, yC = process_lookup_id(lookup_idTwo, False)
            if xC is None and yC is None:
                # pyautogui.press("down", presses=12)
                # time.sleep(1)
                answer = None
                x1, y1 = find_and_click_image(
                    "mergeConflictImages/start_date.png", 0, 0, "NULL", True
                )
                guess = extract_text_from_coordinates(
                    x1 - 40, y1 + 11, x1 + 40, y1 + 40
                )
                x2, y2 = find_and_click_image(
                    "mergeConflictImages/end_date.png", 0, 0, "NULL", True
                )
                guessTwo = extract_text_from_coordinates(
                    x2 - 40, y2 + 11, x2 + 40, y2 + 40
                )
                defaultGuess = f"i {guess}"
                if guessTwo != "":
                    defaultGuess = f"i {guess} {guessTwo}"
                while True:
                    response = pyautogui.prompt(
                        text="n = no; i = opt in; o = opt out; c = no contact; dnc; q = stop; e",
                        title="Command",
                        default=defaultGuess,
                    )
                    commands = response.split(",")
                    for command in commands:
                        parts = command.strip().split(" ")
                        answer = parts[0] if len(parts) > 0 else None
                        start_date = parts[1] if len(parts) > 1 else None
                        end_date = parts[2] if len(parts) > 2 else None
                        process_answer(answer, start_date, end_date, saveOne, saveTwo)
                        # No NDO Direct Mail Fundraising
                    if commands[-1].strip().split(" ")[0] == "n":
                        break
                    if commands[-1].strip().split(" ")[0] != "e":
                        defaultGuess = "e"
                        continue
                    if commands[-1].strip().split(" ")[0] == "e":
                        delete_form()
                        write_to_file("lookup_ids.txt", f"{saveOne}\n{saveTwo}\n")
                        write_to_file(
                            "lookup_ids_with_names.txt",
                            f"{saveOne} - {namesOne}\n{saveTwo} - {namesTwo}\n",
                        )
                    break
            else:
                write_to_file("lookup_ids.txt", f"{saveOne} {xC}\n{saveTwo} {xC}\n")
        else:
            write_to_file("lookup_ids.txt", f"{saveOne} {xC}\n{saveTwo} {xC}\n")


if __name__ == "__main__":
    main()
