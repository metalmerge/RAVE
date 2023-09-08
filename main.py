# Author: Dimitry Ermakov, minimum time: 30.85 seconds
# TODO, fix times, click streamline by having it reconizgize only 1 interaction
import random
import sys
import threading
import time
from datetime import datetime
import pytesseract
import keyboard
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")
noted_date = "1/"


def click_on_images(image_path):
    try:
        # Locate the center of the image on the screen
        image_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.75)
        print(image_location)
        if image_location is not None:
            # Move the mouse to the center of the image and click
            # pyautogui.moveTo(image_location)
            # pyautogui.click()
            return True
        else:
            # print(f"Image '{image_path}' not found on the screen.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def down_command():
    for _ in range(0, 7):
        pyautogui.press("down")


def cord_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        sys.exit()


def cord_click_type(x, y, text):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.typewrite(text)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        sys.exit()
    return True


def get_to_dead_page():
    cord_click(271, 228)  # click on the search bar
    pyautogui.click()
    time.sleep(1.25)
    cord_click(290, 377)  # click on constituents updates
    time.sleep(5)
    cord_click(360, 490)  # click on the first constituent
    time.sleep(5)
    cord_click(262, 691)  # interactions button
    click_on_images("target/interactions.png")


def click_on_first_interaction():
    cord_click(420, 748)  # click on first pending
    time.sleep(0.5)
    cord_click(288, 772)  # click on the edit button
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
    cord_click(1035, 635)
    click_on_images("target/comments.png")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Note: Not Researched - DE")
    time.sleep(0.02)
    newdate = pyautogui.prompt(text="", title="Noted Date?", default="1/")
    if newdate != "1/":
        noted_date = newdate
    cord_click(857, 826)
    time.sleep(0.02)
    cord_click(912, 828)  # save button
    return newdate
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
    pyautogui.write("Note: Duplicate - DE")
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
        pyautogui.write(formatted_date)
    elif noted_date != "1/":
        pyautogui.write(noted_date)
    time.sleep(0.02)
    cord_click(857, 514)
    time.sleep(0.02)
    cord_click(772, 562)  # reason
    time.sleep(0.02)
    cord_click(736, 571)  # save button
    # cord_click(834, 579)  # cancel button


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    # pyautogui.prompt(
    #     text="Press OK when you are ready to capture the textbox.",
    #     title="Capture Textbox",
    # )
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    # textbox_image.show()
    extracted_text = pytesseract.image_to_string(textbox_image)
    return extracted_text.strip()


def move_to_communications():
    cord_click(73, 370)  # consituents
    time.sleep(6)
    cord_click(497, 826)  # communications
    time.sleep(0.02)


def opt_out_form():
    time.sleep(0.25)
    cord_click(703, 442)
    time.sleep(1)
    pyautogui.write("Imprimis")
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


def interactions_section():
    time.sleep(3)
    down_command()
    time.sleep(0.25)
    click_on_first_interaction()

    num = pyautogui.prompt(
        text="",
        title="0 = one interaction, 1 = >1 intereactions, -1 to quit",
        default="0",
    )

    cord_click(857, 826)

    if int(num) == -1:
        print("Quit")
        sys.exit()
    elif int(num) == 0:
        confirm()
        time.sleep(1.5)
        cord_click(286, 546)  # personal info click
        time.sleep(1)
        cord_click(529, 646)  # mark deceased button
        time.sleep(1)
    elif int(num) > 0:
        confirm()
        click_on_images("target/screen17.png")
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
            break

        get_to_dead_page()
        interactions_section()
        deceased_form()
        time.sleep(2)
        move_to_communications()

        for _ in range(0, 2):
            pyautogui.press("down")
        time.sleep(0.25)
        cord_click(382, 822)  # click on add for communications
        opt_out_form()


if __name__ == "__main__":
    threading.Thread(target=keyboard.wait, args=("esc",)).start()
    main()
