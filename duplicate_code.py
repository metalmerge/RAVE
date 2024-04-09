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


def form_adder(text, start_date, end_date):
    find_and_click_image("images_duplicate/communications.png")
    find_and_click_image("windowsTarget/add.png")
    time.sleep(3)
    # find_and_click_image("windowsTarget/solicit_code.png")
    # time.sleep(1)
    
    keyboard.write(text)
    time.sleep(1)
    pyautogui.press("tab")
    if start_date is not None:
        keyboard.write(start_date)
    pyautogui.press("tab")
    if end_date is not None:
        keyboard.write(end_date)
    pyautogui.press("tab", presses=2)
    pyautogui.press("enter")
    time.sleep(3)
    find_and_click_image("images_duplicate/dup_review.png")
    time.sleep(2)
    pyautogui.press("down", presses=12)


def is_date(date_str):
    try:
        parts = date_str.split("/")
        if len(parts) != 3:
            return False
        month, day, year = map(int, parts)
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        if year < 1000:
            return False
        return True
    except ValueError:
        return False


def extract_text_with_conditions(image_path, x_offset, y_offset, bias=0):
    attempts = 0
    extracted_text = ""
    x, y = find_and_click_image(image_path, up_or_down="NULL")
    print(x, y)
    while (extracted_text == "" or not is_date(extracted_text)) and attempts < 30:
        extracted_text = extract_text_from_coordinates(
            x + x_offset,
            y + y_offset + bias,
            x + x_offset + 100,
            y + y_offset + bias + 25,
        ).replace("(", "")
        print(f"Text: {extracted_text}")
        attempts += 1
    if attempts >= 30:
        play_sound("audio/alert_notification.mp3")
        extracted_text = pyautogui.prompt(title="fix", default=f"{extracted_text}")
    return extracted_text


def process_answer(answer, start_date, end_date):
    if start_date and "c" in start_date:
        bias = (int(start_date[1]) - 1) * 25
        start_date = extract_text_with_conditions(
            "images_duplicate/start_date.png", -45, 45, bias
        )

    if end_date and "c" in end_date:
        bias = (int(end_date[1]) - 1) * 25
        end_date = extract_text_with_conditions(
            "images_duplicate/end_date.png", -45, 45, bias
        )

    if answer == "add":
        add3 = extract_text_with_conditions("images_duplicate/add_start.png", -58, 13)
        opt_form(add3, end_date, True)
    elif answer == "add2":
        add4 = extract_text_with_conditions(
            "images_duplicate/source_target.png", 755, 36
        )
        opt_form(add4, end_date, True)
    elif answer == "q":
        find_and_click_image("images_duplicate/comment.png", 0, 25)
        find_and_click_image("windowsTarget/sites.png")
        pyautogui.press("tab", presses=2)
        pyautogui.press("enter", presses=2)
        keyboard.write("DE")  # Make dynamic TODO
        pyautogui.press("tab", presses=2)
        pyautogui.press("enter")
        sys.exit()
    elif answer == "i":
        opt_form(start_date, end_date, True)
    elif answer == "o":
        opt_form(start_date, end_date, False)
    elif answer == "ntm":
        form_adder("No Text Messages", start_date, end_date)
    elif answer == "nc":
        form_adder("No Contact", start_date, end_date)
    elif answer == "np":
        form_adder("No Postal Mailings", start_date, end_date)
    elif answer == "ndo":
        form_adder("No NDO Direct Mail Fundraising", start_date, end_date)
    elif answer == "ne":
        form_adder("No Email", start_date, end_date)
    elif answer == "io":
        form_adder("Imprimis Only", start_date, end_date)
    elif answer == "ni":
        form_adder("No Imprimis", start_date, end_date)
    elif answer == "nm":
        form_adder("No NDO Money Enclosed Mailings", start_date, end_date)
    elif answer == "cyea":
        form_adder("CYEA Only", start_date, end_date)
    elif answer.isdigit():
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
        print(start_date)
        keyboard.write(start_date)
    pyautogui.press("tab")
    if end_date is not None:
        print(end_date)
        keyboard.write(end_date)
    pyautogui.press("tab", presses=7)  # TODO test
    pyautogui.press("enter")
    # time.sleep(3)
    # find_and_click_image(PRIMARY_EMAIL, up_or_down="NULL")
    # pyautogui.press("down", presses=12)
    # time.sleep(1)


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
    x, y = find_and_click_image(
        "mergeConflictImages/constitencies.png", up_or_down="NULL"
    )
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
    keyboard.write("DE")  # Make dynamic TODO
    pyautogui.press("tab", presses=2)
    pyautogui.press("enter")
    # find_and_click_image("images_duplicate/save.png")
    time.sleep(1)
    find_and_click_image("images_duplicate/comment.png", 0, 0, "NULL")
    find_and_click_image("images_duplicate/return.png")


def print_string_difference_and_similarity(string1, string2):
    diff_count = 0
    total_chars = min(len(string1), len(string2))
    match_count = 0

    for i, (char1, char2) in enumerate(zip(string1, string2)):
        if (
            char1 != char2
            and (i == 0 or char1 != string1[i - 1])
            and (i == len(string1) - 1 or char1 != string1[i + 1])
        ):
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
    log_file = "time_log_duplicate.txt"
    print(f"{duration:.2f}")
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def codes_num_finder():
    time.sleep(1)
    x, y = find_and_click_image("images_duplicate/review_sol.png", up_or_down="NULL")
    print(x, y)
    amount = None
    x = int(x)
    y = int(y)
    while not amount:
        amount = extract_digits_from_text(
            extract_text_from_coordinates(x + 80, y - 20, x + 120, y + 20)
        )
        print(f"Solicit Codes: {amount}")
    return int(amount)


def opt_finder(bias=0):
    time.sleep(1)
    x, y = find_and_click_image("images_duplicate/pref.png", up_or_down="NULL")
    print(x, y)
    x = int(x)
    y = int(y)
    amount = None
    attempts = 0
    while not amount and attempts < 20:
        amount = extract_text_from_coordinates(
            x - 45, y + 45 + bias, x + 30, y + 70 + bias
        )
        if amount:
            print(f"opt one: {amount}")
        attempts += 1
    if amount == "Opt-out" or amount == "opt-out":
        amount = False
    elif amount == "":
        amount = None
    else:
        amount = True
    return amount


from datetime import datetime, timedelta


def subtract_one_day(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_string, "%m/%d/%Y")
        except ValueError:
            print("Failed to parse date: ", date_string)
            return date_string

    previous_day = date_obj - timedelta(days=1)
    previous_day_string = previous_day.strftime("%m/%d/%Y")

    return previous_day_string


def main():
    global delay, x_scale, y_scale, cutOffBottomY, cutOffTopY, CRM_cords
    x_scale, y_scale, cutOffBottomY = get_screen_dimensions()
    with open("bias.txt", "r") as file:
        bias = int(file.read().strip()) * 25
    add1 = -1
    add2 = 25
    play = 0
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while True:
        print(bias)
        find_and_click_image("windowsTarget/updates.png", 0, 25)
        while True:
            find_and_click_image(
                "images_duplicate/target_lookup_id.png", -30, (27 + bias)
            )  # +25 for bias
            if allowed_constituencies() == -1:
                pyautogui.alert(
                    text="This constituent is not allowed to be solicited",
                    title="Error",
                    button="OK",
                )
            x5, y5 = find_and_click_image("images_duplicate/return.png", 0, 0, "NULL")
            add5 = ""
            attempts = 0
            print(x5, y5)
            while (add5 == "" or add5.index("%") == -1) and attempts < 30:
                add5 = extract_text_from_coordinates(
                    x5 + (-50), y5 + (35), x5 + (30), y5 + (65)
                )
                print(f"Text: {add5}")
                attempts += 1
            if attempts >= 30:
                add5 = pyautogui.prompt(title="fix percent", default=f"-1")
                if add5 == "0":
                    add5 == "100.00%"
            pyautogui.press("down", presses=5)
            if add5 != "100.00%" and add5 != "10.00%":
                time.sleep(1)
                x2, y2 = find_and_click_image(
                    "images_duplicate/source_target.png", 0, 51
                )
                x1, y1 = find_and_click_image(
                    "images_duplicate/target_select.png", 0, 50
                )
                y1 -= 50
                y2 -= 50
                attempts = 0
                if add1 != add2:
                    add1 = "0"
                    add2 = 0
                    play_sound("audio/alert_notification.mp3")
                    play = -1
                    add = pyautogui.prompt(
                        text="Addresses Correct?",
                        title="Addresses",
                        default="y",
                    )
                    if add == "z":
                        with open("bias.txt", "r+") as file:
                            bias_value = int(file.read().strip()) + 1
                            file.seek(0)
                            file.write(str(bias_value))

                        bias = bias_value
                        break
                else:
                    add = "y"

                find_and_click_image("images_duplicate/target_select.png", 0, 50)
                time.sleep(1)
                find_and_click_image("images_duplicate/source_target.png", 0, 51)
                if add == "z":
                    play_sound("audio/alert_notification.mp3")
                    play = -1
                    additional = pyautogui.prompt(
                        text="Addresses Correct?",
                        title="Addresses",
                        default="y",
                    )
                    if additional == "y":
                        find_and_click_image(
                            "images_duplicate/target_select.png", 0, 50
                        )
                        time.sleep(1)
                        find_and_click_image(
                            "images_duplicate/source_target.png", 0, 51
                        )
            answer = None

            while True:

                option_mapping = {
                    "1": ("2,2,", 3, "0", True),
                    "2": ("i c3 x,3,3,add2,", 3, "0", False),
                    "3": ("i c3,3,3,", 3, "22", False),
                    "4": ("i c2,2,2,", 2, "0", None),
                    "5": ("2,2,add,", 3, "0", True),
                    "6": ("2,2,2,add,", 4, "30", False),
                    "7": ("2,", 2, "0", True),
                    "8": ("", 1, "0", False),
                    "9": ("o c2,3,3,add2,", 3, "31", True),
                    "10": ("2,add,", 2, "0", False),
                    "11": ("3,3,add,", 4, "0", False),
                    "12": ("3,add2,", 3, "0", None),
                    "13": ("2,2,2,2,add,", 5, "0", False),
                    "14": ("3,3,3,add,", 5, "0", True),
                    "15": ("o c3,4,4,add,", 4, "0", True),
                    "16": ("2,2,add2,", 3, "0", True),  # None
                    "17": ("3,3,3,3,add,", 5, "0", False),
                    "18": ("o c3,3,3,3,add2,", 4, "0", True),
                    "19": ("1,add2,", 1, "0", None),
                    "20": ("1,1,1,1,i x,o x,add2,", 4, "0", True),
                    "21": ("4,4,4,4,", 6, "0", False),  # None
                    "22": ("o c1,2,2,add2,", 2, "0", False),
                    "23": ("o c2,2,2,2,add,", 3, "0", None),
                    "24": ("1,o c2,2,2,2,add,", 4, "0", False),
                    "25": ("1,o c2,2,2,2,add2,", 4, "0", False),
                    "26": ("i c3 x,3,3,add,", 3, "0", False),
                }



                code_num = codes_num_finder()
                opt_one = ""
                opt_two = ""
                opt_one = opt_finder()
                if code_num > 1:
                    opt_two = opt_finder(25)

                if code_num == 1 and opt_one == None:
                    defaultGuess = option_mapping["19"][0]
                elif code_num == 1:
                    defaultGuess = option_mapping["8"][0]
                elif code_num == 2 and opt_one == False and opt_two == None:
                    defaultGuess = option_mapping["10"][0]
                elif code_num == 2 and (
                    (opt_one == True and opt_two == None)
                    or (opt_one == True and opt_two == True)
                ):
                    defaultGuess = option_mapping["7"][0]
                elif code_num == 2 and opt_one == None:
                    defaultGuess = option_mapping["4"][0]
                elif code_num == 2 and opt_one == False:
                    defaultGuess = option_mapping["10"][0]
                elif code_num == 3 and opt_one == True and opt_two == None:
                    defaultGuess = option_mapping["16"][0]
                elif code_num == 3 and opt_one == False:
                    defaultGuess = option_mapping["3"][0]
                elif code_num == 3 and opt_one == True:
                    defaultGuess = option_mapping["9"][0]
                elif code_num == 3 and opt_one == None and opt_two == False:
                    defaultGuess = option_mapping["23"][0]
                elif code_num == 3 and opt_one == None:
                    defaultGuess = option_mapping["12"][0]
                elif code_num == 4 and opt_one == True and opt_two == None:
                    defaultGuess = option_mapping["18"][0]
                elif code_num == 4:
                    defaultGuess = option_mapping["6"][0]
                elif code_num == 5 and opt_one == None and opt_two == False:
                    defaultGuess = option_mapping["14"][0]
                elif code_num == 5 and opt_one == False and opt_two == None:
                    defaultGuess = option_mapping["14"][0]
                elif code_num == 5 and opt_one == True and opt_two == None:
                    defaultGuess = option_mapping["18"][0]
                elif code_num == 5 and opt_one == False:
                    defaultGuess = option_mapping["13"][0]
                elif code_num == 5 and opt_one == True:
                    defaultGuess = option_mapping["13"][0]
                elif code_num == 6:
                    defaultGuess = option_mapping["21"][0]
                else:
                    defaultGuess = ""
                text = "\n".join(
                    [
                        f"{key}| {value[0]}| Commas: {value[1]}| Time: {value[2]}| Opt-in/out: {value[3]}"
                        for key, value in option_mapping.items()
                    ]
                )

                if play == 0:
                    play_sound("audio/alert_notification.mp3")
                option = pyautogui.prompt(
                    text=text,
                    default=defaultGuess,
                )

                if option in option_mapping:
                    option = option_mapping[option][0]
                if option == "q":
                    sys.exit()
                elif option == "z":
                    print("Skip")
                    with open("bias.txt", "r+") as file:
                        bias_value = int(file.read().strip())+1
                        file.seek(0)
                        file.write(str(bias_value))

                    bias = bias_value
                    find_and_click_image("windowsTarget/updates.png",0,25)
                    break
                start_index = 0
                while option.find("x", start_index) != -1:
                    print(option)
                    index = option.find("x", start_index)
                    guessX = extract_text_with_conditions(
                        "images_duplicate/start_date.png", -45, 45
                    )
                    guessX = subtract_one_day(guessX)
                    print(guessX)
                    retro_date = pyautogui.prompt(
                        text="Replace x at index {}: ".format(index), default=guessX
                    )
                    option = option[:index] + retro_date + option[index + 1 :]
                    start_index = index + 1

                start_time = time.time()

                commands = option.split(",")
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
