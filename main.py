# @Dimitry Ermakov
# @09/09/2023

import random
import sys
import threading
import time
from datetime import datetime

import keyboard
import pyautogui
import pytesseract

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")
noted_date = "1/"


def contains_digits(text):
    for char in text:
        if char.isdigit():
            return True
    return False


def cord_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        sys.exit()


def get_to_dead_page():
    cord_click(271, 228)  # click on the search bar
    time.sleep(1.25)
    cord_click(290, 377)  # click on constituents updates
    time.sleep(5)
    cord_click(360, 490)  # click on the first constituent


def click_on_first_interaction():
    cord_click(424, 789)  # click on first pending
    time.sleep(0.5)
    cord_click(300, 822)  # click on the edit button
    time.sleep(0.75)


def confirm():
    global noted_date
    cord_click(687, 250)
    time.sleep(0.02)
    cord_click(535, 297)
    time.sleep(0.02)
    cord_click(1022, 337)
    time.sleep(0.02)
    cord_click(924, 526)
    time.sleep(0.02)
    if contains_digits(extract_text_from_coordinates(750, 1050, 2100, 1300)):
        noted_date = pyautogui.prompt(text="", title="Noted Date?", default="1/")

    time.sleep(0.02)
    cord_click(1035, 635)
    pyautogui.press("enter")
    time.sleep(0.02)
    pyautogui.press("enter")
    time.sleep(0.02)
    keyboard.write("Note: Not Researched - DE")
    time.sleep(1)
    cord_click(857, 826)
    time.sleep(0.02)
    cord_click(912, 828)  # save button
    # cord_click(1015, 825)  # cancel button


def decline():
    # time.sleep(1)
    # cord_click(421, (696 + (scalar - 1) * 25))
    # time.sleep(5)
    # cord_click(306, 725 + (scalar - 1) * 25)
    # time.sleep(5)

    # form
    cord_click(687, 252)
    time.sleep(0.02)
    cord_click(523, 338)
    time.sleep(0.02)
    cord_click(1023, 338)
    time.sleep(0.02)
    cord_click(924, 526)
    time.sleep(0.02)
    cord_click(1035, 635)
    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - DE")
    time.sleep(0.02)
    cord_click(912, 828)  # save button
    # cord_click(1015, 825)  # cancel button
    time.sleep(0.5)
    end = pyautogui.prompt(
        text="", title="More duplicates?, 1 = yes, 0 = no", default="0"
    )
    cord_click(194, 664)  # safe corner
    return end


def deceased_form():
    global noted_date
    cord_click(716, 458)  # date
    time.sleep(0.02)
    if noted_date == "1/":
        keyboard.write(formatted_date)
    elif noted_date != "1/":
        keyboard.write(noted_date)
    time.sleep(0.02)
    cord_click(857, 514)
    time.sleep(0.02)
    cord_click(772, 562)  # reason
    time.sleep(0.02)
    cord_click(736, 571)  # save button
    # cord_click(834, 579)  # cancel button


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    # textbox_image.show()
    # textbox_image.save("textbox.png")
    extracted_text = pytesseract.image_to_string(textbox_image)
    print(extracted_text.strip())
    return extracted_text.strip()


def move_to_communications():
    cord_click(73, 370)  # consituents
    time.sleep(6)
    cord_click(497, 826)  # communications
    time.sleep(0.02)


def opt_out_form():
    time.sleep(0.25)
    cord_click(703, 442)
    time.sleep(0.5)
    keyboard.write("Imprimis")
    time.sleep(0.5)
    cord_click(572, 442)  # wait
    time.sleep(0.5)

    cord_click(850, 505)  # date button
    time.sleep(0.02)
    cord_click(748, 686)  # today

    time.sleep(0.02)
    cord_click(850, 476)  # tab
    time.sleep(0.02)
    cord_click(733, 515)  # opt out
    time.sleep(0.02)
    # cord_click(698, 642)
    # time.sleep(1)
    cord_click(849, 637)
    time.sleep(0.02)
    cord_click(698, 706)
    time.sleep(0.02)
    cord_click(636, 642)
    time.sleep(0.02)
    for _ in range(0, 3):
        pyautogui.press("down")

    time.sleep(0.02)
    cord_click(737, 820)  # save
    time.sleep(1.5)
    # cord_click(272, 225)  # click on the search bar


def interactions_section(num):
    time.sleep(4)
    for _ in range(0, 6):
        pyautogui.press("down")
    time.sleep(0.25)
    click_on_first_interaction()

    if int(num) == 0:
        confirm()
        time.sleep(1.5)
        cord_click(286, 587)  # personal info click
        time.sleep(1)
        cord_click(531, 685)  # mark deceased button
        time.sleep(1)
    elif int(num) > 0:
        confirm()
        time.sleep(1)
        duplicates = True
        while duplicates:
            pyautogui.prompt(
                text="",
                title="Enter when you are at the decline form",
                default="0",
            )
            cord_click(857, 826)
            if decline() == "0":
                duplicates = False
            pyautogui.prompt(
                text="",
                title="Enter when you are at the deceased form",
                default="0",
            )
            cord_click(639, 515)  # wait
            time.sleep(1)


def main():
    job = 0
    while True:
        job = pyautogui.prompt(text="", title="Enter the Task, -1 to quit", default="0")
        if job == "-1":
            sys.exit()
        cord_click(271, 173)
        get_to_dead_page()
        time.sleep(5)
        if extract_text_from_coordinates(420, 1350, 620, 1400) == "Interactions: 1":
            num = 0
        else:
            num = 1
        time.sleep(0.25)
        cord_click(262, 691)  # interactions button
        interactions_section(num)
        deceased_form()
        time.sleep(3)
        move_to_communications()

        for _ in range(0, 2):
            pyautogui.press("down")
        time.sleep(0.25)
        cord_click(382, 822)  # click on add for communications
        opt_out_form()


if __name__ == "__main__":
    threading.Thread(target=keyboard.wait, args=("esc",)).start()
    main()
