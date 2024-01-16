# @Dimitry Ermakov
# @12/06/2023
import time
import pyperclip
import keyboard
import pyautogui
from datetime import datetime
from main_shared_functions import cord_click

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
first_half = True


def find_and_click_image(image_filename, biasx=0, biasy=0, up_or_down=None):
    global cutOffTopY, delay, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, confidence, PRIMARY_EMAIL, first_half
    box = None
    if first_half and image_filename == "windowsTarget/constituteSearch.png":
        start = 0
        finish = 960
    if first_half == False and image_filename != "windowsTarget/constituteSearch.png":
        start = 910
        finish = 1920
    else:
        start = 0
        finish = 1920
    if image_filename == "windowsTarget/constituteSearch.png":
        confidence = 0.8
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
        if box is None and up_or_down:
            factor = 14 if up_or_down == "up" else -14
            pyautogui.scroll(factor)
            time.sleep(delay * 2)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy

    if image_filename != PRIMARY_EMAIL:
        cord_click((x, y))


def end_time_recording(start_time):
    end_time = time.time()
    duration = end_time - start_time
    log_file = "time_logs/notifcationsLog.txt"
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
    global cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, delay, PRIMARY_EMAIL, first_half
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowsTarget/blackbaudCRM.png")
    while True:
        lookup_idOne, lookup_idTwo = pyautogui.prompt(
            text="Enter LookUp IDs:",
            title="LookUp IDs",
            # default="(ex - 11/22/2023, Elizabeth Dolman)",
        ).split(" ")

        # Convert to integers
        lookup_idOne = int(lookup_idOne)
        lookup_idTwo = int(lookup_idTwo)

        # lookup_idTwo is on the right and is the smaller target
        if lookup_idOne < lookup_idTwo:
            lookup_idOne, lookup_idTwo = lookup_idTwo, lookup_idOne
        if lookup_idOne == "-1" or lookup_idTwo == "-1":
            break
        print(f"{lookup_idOne} : {lookup_idTwo}")

        start_time = time.time()
        # part 1
        find_and_click_image("windowsTarget/constituteSearch.png")
        time.sleep(1)
        find_and_click_image("mergeConflictImages/lookupID.png")
        time.sleep(0.25)
        keyboard.press_and_release("ctrl+a")
        time.sleep(0.25)
        keyboard.write(str(lookup_idOne))
        pyautogui.press("enter")
        find_and_click_image("windowsTarget/cityStateZIP.png")
        find_and_click_image(PRIMARY_EMAIL)
        for _ in range(12):
            pyautogui.press("down")
        # TODO old code
        # copy and paste into prompt ID's
        # break into half screens
        # Size(width=1920, height=1080)
        # give a buffer of 100

        # get to page and then down 12
        # image.png
        # find & get all details and then try to make timeline
        # -710
        # 27 height whole, so 13 up and down

        # opt = -645 to -580
        # start = -540 to -360
        # end = -348 to -254

        # log the numbers in txt
        # Wait for imprintis before down
        # control a before typing ID
        first_half = False
        find_and_click_image("windowsTarget/constituteSearch.png")
        time.sleep(1)
        find_and_click_image("mergeConflictImages/lookupID.png")
        time.sleep(0.25)
        keyboard.press_and_release("ctrl+a")
        time.sleep(0.25)
        keyboard.write(str(lookup_idTwo))
        pyautogui.press("enter")
        find_and_click_image("windowsTarget/cityStateZIP.png")
        find_and_click_image(PRIMARY_EMAIL)
        for _ in range(12):
            pyautogui.press("down")

        end_time_recording(start_time)
        with open("lookup_ids.txt", "a") as f:
            f.write(f"{lookup_idOne}\n{lookup_idTwo}\n")


if __name__ == "__main__":
    main()
