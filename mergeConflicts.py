# @Dimitry Ermakov
# @12/06/2023
import time
import pyperclip
import keyboard
import pyautogui
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
    image_filename, biasx=0, biasy=0, up_or_down=None, first_half=None
):
    global cutOffTopY, delay, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, confidence
    box = None
    if first_half:
        start = 0
        finish = 960
    elif first_half == False:
        start = 700
        finish = 1920
    elif first_half == None:
        start = 0
        finish = 1920
    if image_filename == "windowsTarget/constituteSearch.png":
        confidence = 0.75
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(
                start,
                cutOffTopY,
                finish,
                round(cutOffBottomY * 2 * y_scale),
            ),
        )
        time.sleep(delay * 5)
        print(image_filename)
        if box is None and up_or_down and up_or_down != "NULL":
            factor = 200 if up_or_down == "up" else -200
            pyautogui.scroll(factor)
            time.sleep(delay * 2)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy

    if up_or_down != "NULL":
        cord_click((x, y))
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
    print(string[:2] + "/" + string[2] + string[3] + "/" + string[4:])
    return string[:2] + "/" + string[2] + string[3] + "/" + string[4:]


def main():
    global cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, delay, PRIMARY_EMAIL, namesOne, namesTwo
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while True:
        lookup_idOne, lookup_idTwo = get_lookup_ids()
        lookup_idOne = int(lookup_idOne)
        lookup_idTwo = int(lookup_idTwo)
        saveOne = lookup_idOne
        saveTwo = lookup_idTwo
        # lookup_idTwo is on the right and is the smaller target
        if lookup_idOne < lookup_idTwo:
            lookup_idOne, lookup_idTwo = lookup_idTwo, lookup_idOne
        if lookup_idOne == "-1" or lookup_idTwo == "-1":
            break
        print(f"{saveOne}\n{saveTwo}")

        # part 1
        find_and_click_image("windowsTarget/constituteSearch.png", 0, 0, None, True)
        time.sleep(1)
        find_and_click_image("mergeConflictImages/lookupID.png")
        time.sleep(0.25)
        keyboard.press_and_release("ctrl+a")
        time.sleep(0.25)
        keyboard.write(str(lookup_idOne))
        pyautogui.press("enter")
        find_and_click_image("windowsTarget/cityStateZIP.png", 0, 2)
        find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", True)
        for _ in range(12):
            pyautogui.press("down")
        time.sleep(1)
        if codes_num_finder() != 0:
            # Size(width=1920, height=1080)

            # find & get all details and then try to make timeline
            # -710
            # 27 height whole, so 13 up and down
            # opt = -645 to -580
            # start = -540 to -360
            # end = -348 to -254

            find_and_click_image(
                "windowsTarget/constituteSearch.png", 0, 0, None, False
            )
            time.sleep(1)
            find_and_click_image("mergeConflictImages/lookupID.png")
            time.sleep(0.25)
            keyboard.press_and_release("ctrl+a")
            time.sleep(0.25)
            keyboard.write(str(lookup_idTwo))
            pyautogui.press("enter")
            find_and_click_image("windowsTarget/cityStateZIP.png", 0, 2)
            find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
            for _ in range(12):
                pyautogui.press("down")
            time.sleep(1)
            answer = None
            x1, y1 = find_and_click_image(
                "mergeConflictImages/start_date.png", 0, 0, "NULL", True
            )
            guess = extract_text_from_coordinates(x1 - 40, y1 + 11, x1 + 40, y1 + 40)
            x2, y2 = find_and_click_image(
                "mergeConflictImages/end_date.png", 0, 0, "NULL", True
            )
            guessTwo = extract_text_from_coordinates(
                x2 - 40, y2 + 11, x2 + 40, y2 + 40
            )  # TODO untested
            defaultGuess = f"i {guess}"
            if guessTwo != "":
                defaultGuess = f"i {guess} {guessTwo}"
            while answer != "" and answer != "n":
                response = pyautogui.prompt(
                    text="n = no; i = opt in; o = opt out; c = no contact; dnc; q = stop",
                    title="Confirm IDs",
                    default=defaultGuess,
                )
                parts = response.split(" ")
                answer = parts[0] if len(parts) > 0 else None
                start_date = (parts[1]) if len(parts) > 1 else None
                end_date = (parts[2]) if len(parts) > 2 else None
                if answer == "n":
                    with open("lookup_ids.txt", "a") as f:
                        f.write(f"{saveOne} XXX\n{saveTwo} XXX\n")
                elif answer == "q":
                    delete_form()
                    with open("input.txt", "a") as f:
                        f.write(f"{saveOne}\n{saveTwo}\n")
                    sys.exit()
                elif answer == "i":
                    opt_form(start_date, end_date, True)
                elif answer == "o":
                    opt_form(start_date, end_date, False)
                elif answer == "c":
                    no_contact_form(start_date, end_date)
                elif answer == "dnc":
                    find_and_click_image(
                        "mergeConflictImages/noContact.png", 0, 0, None, False
                    )
                    time.sleep(1)
                    find_and_click_image(
                        "mergeConflictImages/delete.png", 0, 0, None, False
                    )
                    find_and_click_image(
                        "mergeConflictImages/yes.png", 0, 0, None, False
                    )
                    time.sleep(1)
                    find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", False)
                    for _ in range(12):
                        pyautogui.press("down")
                defaultGuess = ""
            if answer == "":
                delete_form()
                with open("lookup_ids.txt", "a") as f:
                    f.write(f"{saveOne}\n{saveTwo}\n")
                with open("lookup_ids_with_names.txt", "a") as f:
                    f.write(f"{saveOne} - {namesOne}\n{saveTwo} - {namesTwo}\n")
        else:
            with open("lookup_ids.txt", "a") as f:
                f.write(f"{saveOne} XXX\n{saveTwo} XXX\n")


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
    for _ in range(12):
        pyautogui.press("down")


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
    for _ in range(12):
        pyautogui.press("down")


def delete_form():
    for _ in range(codes_num_finder()):
        find_and_click_image(
            "mergeConflictImages/code pref delete.png", 0, 25, None, True
        )
        find_and_click_image("mergeConflictImages/delete.png", 0, 0, None, True)
        find_and_click_image("mergeConflictImages/yes.png", 0, 0, None, True)
        time.sleep(1)
        find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL", True)
        for _ in range(12):
            pyautogui.press("down")
        time.sleep(1)


def get_lookup_ids():
    global namesOne, namesTwo
    try:
        with open("input.txt", "r+") as f:
            lines = f.readlines()
            if not lines:
                return pyautogui.prompt(
                    text="Enter LookUp IDs:",
                    title="LookUp IDs",
                ).split(" ")
            lookup_idOne, lookup_idTwo = lines[:2]
            f.seek(0)
            f.writelines(lines[2:])
            f.truncate()
            # lookup_idOne = namesOne # TODO incorporate names?
            # lookup_idTwo = namesTwo
            # print(lookup_idOne)
            # lookup_idOne = extract_digits_from_text(lookup_idOne)
            # lookup_idTwo = extract_digits_from_text(lookup_idTwo)
    except FileNotFoundError:
        return pyautogui.prompt(
            text="Enter LookUp IDs:",
            title="FileNotFoundError",
        ).split(" ")

    return lookup_idOne.strip(), lookup_idTwo.strip()


if __name__ == "__main__":
    main()
