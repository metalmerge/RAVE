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
        confidence=.9
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

def contains_non_digits_or_slash(input_string):
    for char in input_string:
        if not (char.isdigit() or char == "/"):
            return True
    return False
def process_answer(answer, start_date, end_date):
    print(answer)
    attempts = 0
    add1=""
    if start_date:
        if "c" in start_date:
            bias = (int(start_date[1])-1)*25
            x1, y1 = find_and_click_image("images_duplicate/start_date.png",0,0,"NULL")
            print(x1,y1)
            while add1 == "" and attempts < 30:
                add1 = extract_text_from_coordinates(x1 + (-45), y1 + (45+(bias)), x1 + (47), y1 + (68+bias)).replace('‘','').replace('(','')
                print(f"Text: {add1}")
                attempts += 1
            start_date = add1
        attempts = 0
        add2=""
    if end_date:
        if "c" in end_date:
            bias = (int(end_date[1])-1)*25
            x2, y2 = find_and_click_image("images_duplicate/end_date.png",0,0,"NULL")
            print(x2,y2)
            while add2 == "" and attempts < 30:
                add2 = extract_text_from_coordinates(x2 + (-45), y2 + (45+(bias)), x2 + (47), y2 + (68+bias))
                print(f"Text: {add2}")
                attempts += 1
            end_date = add2
    if answer == "add":
        attempts = 0
        add3=""
        x3, y3 = find_and_click_image("images_duplicate/add_start.png",0,0,"NULL")
        print(x3,y3)
        while add3 == "" and attempts < 30 and contains_non_digits_or_slash(add3) == False:
            add3 = extract_text_from_coordinates(x3 + (-58), y3 + (13), x3 + (22), y3 + (38))
            print(f"Text: {add3}")
            attempts += 1
        if attempts > 30:
            add3 = pyautogui.prompt(title="fix", default=f"{add3}")
        opt_form(add3, end_date, True)
    elif answer == "add2":
        attempts = 0
        add4=""
        x4, y4 = find_and_click_image("images_duplicate/source_target.png",0,0,"NULL")
        print(x4,y4)
        while add4 == "" and attempts < 30 and contains_non_digits_or_slash(add4) == False:
            add4 = extract_text_from_coordinates(x4 + (755), y4 + (36), x4 + (844), y4 + (60))
            print(f"Text: {add4}")
            attempts += 1
        if  attempts > 30:
            add4 = pyautogui.prompt(title="fix", default=f"{add3}")
        opt_form(add4, end_date, True)
    elif answer == "q":
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
        pyautogui.press("down",presses=2)
        time.sleep(1)
        delete_specifc_form("images_duplicate/noValidAddress.png")
    elif answer == "dni":
        delete_specifc_form("images_duplicate/no_imprintis.png")
    elif answer.isdigit():
        # if int(answer) >= 3:
        #     pyautogui.press("down",presses=2)
        #     time.sleep(1)
        delete_specifc_form("images_duplicate/review_down.png",0,(80+((int(answer)-1)*25)))




def opt_form(start_date, end_date, opt_in):
    find_and_click_image("images_duplicate/target_select.png", 0, 40)
    if opt_in:
        find_and_click_image("images_duplicate/opt_in_button.png")
    else:
        find_and_click_image("images_duplicate/opt_in_button.png",100)

    time.sleep(3)
    pyautogui.press("tab", presses=2)

    if start_date is not None:
        print(start_date)
        keyboard.write(start_date)
    pyautogui.press("tab")
    if end_date is not None:
        print(end_date)
        keyboard.write(end_date)
    pyautogui.press("tab", presses=7)  # TODO test
    pyautogui.press("enter")
    # time.sleep(3)
    # find_and_click_image(PRIMARY_EMAIL, 0, 0, "NULL")
    # pyautogui.press("down", presses=12)
    # time.sleep(1)


def delete_specifc_form(image,biasx=30,biasy=0):
    while True:
        x, y = find_and_click_image(image,biasx,biasy)
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
        # "Prospect",
        # " Prospect",
        # "prospect",
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
    find_and_click_image("windowsTarget/sites.png")
    pyautogui.press("tab", presses=2)
    pyautogui.press("enter", presses=2)
    keyboard.write("DE") #Make dynamic TODO
    pyautogui.press("tab", presses=2)
    pyautogui.press("enter")
    # find_and_click_image("images_duplicate/save.png")
    time.sleep(1)
    find_and_click_image("images_duplicate/comment.png", 0, 0,"NULL")
    find_and_click_image("images_duplicate/return.png")

def print_string_difference_and_similarity(string1, string2):
    diff_count = 0
    total_chars = min(len(string1), len(string2))
    match_count = 0
    
    for i, (char1, char2) in enumerate(zip(string1, string2)):
        if char1 != char2 and (i == 0 or char1 != string1[i - 1]) and (i == len(string1) - 1 or char1 != string1[i + 1]):
            print(f"Difference found at index {i}: '{char1}' != '{char2}'")
            diff_count += 1
        else:
            match_count += 1
    
    similarity_percent = (match_count / total_chars) * 100
    print(f"Percentage of similarity between the strings: {similarity_percent:.2f}%")
    print(f"Total differences found: {diff_count}")

def end_time_recording(start_time):
    
    end_time = time.time()
    duration = end_time - start_time
    log_file = "dup_time_logs.txt"
    print(f"{duration:.2f}")
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")
def main():
    global delay, x_scale, y_scale, cutOffBottomY, cutOffTopY, CRM_cords
    x_scale, y_scale, cutOffBottomY = get_screen_dimensions()
    bias = 100
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while True:
        find_and_click_image("windowsTarget/updates.png")
        while True:
            find_and_click_image("images_duplicate/target_lookup_id.png", -30, (25+bias)) # +25 for bias
            if allowed_constituencies() == -1:
                pyautogui.alert(
                    text="This constituent is not allowed to be solicited",
                    title="Error",
                    button="OK",
                )
            pyautogui.press("down",presses=5)
            time.sleep(1)
            x1, y1 = find_and_click_image("images_duplicate/target_select.png", 0, 50)
            y1 -= 50
            time.sleep(1.5)
            x2, y2 = find_and_click_image("images_duplicate/source_target.png", 0, 51)
            y2 -= 50
            add1 = "-1"
            add2 = ""
            attempts = 0
            if add1 != add2:
                play_sound("audio/alert_notification.mp3")
                add = pyautogui.prompt(
                    text="Addresses Correct?",
                    title="Addresses",
                    default="y",
                )
                if add == "add":
                    bias += 25
                    break  # Exit the inner loop to click updates again
            else:
                add = "y"
                
            find_and_click_image("images_duplicate/target_select.png", 0, 50)
            time.sleep(1)
            find_and_click_image("images_duplicate/source_target.png", 0, 51)
            if add == "z":
                additional = pyautogui.prompt(
                    text="Addresses Correct?",
                    title="Addresses",
                    default="y",
                )
                if additional == "y":
                    find_and_click_image("images_duplicate/target_select.png", 0, 50)
                    time.sleep(1)
                    find_and_click_image("images_duplicate/source_target.png", 0, 51)
            answer = None
            defaultGuess = f"o c2,3,3,add2,"

            while True:
                response = pyautogui.prompt(
                    text="i = opt in; o = opt out; dnc = delete no contact; dnn = delete NDO; dva = delete no valid address; dni = delete no imprintis; q = stop; e",
                    title="Command",
                    default=defaultGuess,
                )
                start_time = time.time()
                commands = response.split(",")
                for index, command in enumerate(commands):
                    parts = command.strip().split(" ")
                    answer = parts[0] if len(parts) > 0 else None
                    start_date = parts[1] if len(parts) > 1 else None
                    end_date = parts[2] if len(parts) > 2 else None
                    process_answer(answer, start_date, end_date)
                    
                    if index != len(commands) - 1:
                        time.sleep(3)
                if commands[-1].strip().split(" ")[0] != "":
                    defaultGuess = ""
                    continue
                if commands[-1].strip().split(" ")[0] == "":
                    merge_request()
                end_time_recording(start_time)
                break


if __name__ == "__main__":
    main()
