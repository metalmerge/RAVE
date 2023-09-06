import random
import threading
import time
from datetime import datetime
import cv2
import keyboard
import numpy as np
import pyautogui
from PIL import Image
from PIL import __version__ as PIL__version__
import sys

running = True
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")


def find_image_center(image_path):
    # Locate the image on the screen
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.9)

        if location is not None:
            # Get the coordinates of the center of the located image
            center_x = location.left + location.width // 2
            center_y = location.top + location.height // 2
            return center_x, center_y
        else:
            print(f"Image '{image_path}' not found on the screen.")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def click_on_images(image_path):
    try:
        # Locate the center of the image on the screen
        image_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)

        if image_location is not None:
            # Move the mouse to the center of the image and click
            pyautogui.moveTo(image_location)
            pyautogui.click()
            return True
        else:
            print(f"Image '{image_path}' not found on the screen.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def click_and_type(image_path, text):
    try:
        # Locate the center of the image on the screen
        image_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)

        if image_location is not None:
            # Move the mouse to the center of the image and click
            pyautogui.moveTo(image_location)
            pyautogui.click()

            # Type the provided text
            pyautogui.typewrite(text)
            return True
        else:
            print(f"Image '{image_path}' not found on the screen.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def click_on_screen(screen_number):
    global running

    # Define the path to the screenshot
    screenshot_path = f"target/screen{screen_number}.png"
    center_x, center_y = find_image_center(screenshot_path)
    print(f"Center of the image: {center_x}, {center_y}")
    pyautogui.moveTo(center_x, center_y)
    # pyautogui.moveTo(88, 355)
    pyautogui.click(clicks=2, interval=0.25, duration=1)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False
        sys.exit()


def cord_click_type(x, y, text):
    global running

    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.typewrite(text)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False
        sys.exit()
    return True


def cord_click(x, y):
    global running

    pyautogui.moveTo(x, y)
    pyautogui.click()

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False
        sys.exit()


def opt_out_form():
    time.sleep(0.5)
    pyautogui.write("Im")
    time.sleep(0.5)
    cord_click(691, 467)  # select
    time.sleep(0.5)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.write(formatted_date)
    time.sleep(0.5)
    cord_click(850, 474)  # tab
    time.sleep(0.5)
    cord_click(704, 474)  # opt out
    time.sleep(0.5)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("deceased")
    time.sleep(2)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")


def confirm():
    # TODO
    print("confirm")
    cord_click(687, 250)
    time.sleep(0.5)
    cord_click(535, 297)
    time.sleep(0.5)
    cord_click(1022, 337)
    time.sleep(0.5)
    cord_click(924, 526)
    time.sleep(0.5)
    cord_click(1031, 585)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Note: Not Researched - DE")


def decline(scalar):
    # TODO
    print("decline")
    cord_click(420, (748 + (scalar - 1) * 25))
    time.sleep(5)
    cord_click(288, 772 + (scalar - 1) * 25)
    time.sleep(5)

    # form
    cord_click(687, 252)
    time.sleep(5)
    cord_click(523, 338)
    time.sleep(5)
    cord_click(1023, 338)
    time.sleep(5)
    cord_click(924, 526)
    time.sleep(5)
    cord_click(988, 581)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Note: Duplicate - DE")
    time.sleep(5)
    # cord_click(1015, 825)  # cancel button
    cord_click(912, 828)  # save button
    time.sleep(5)
    down_command()


def down_command():
    for x in range(0, 7):
        pyautogui.press("down")


def decease_form():
    cord_click(716, 458)  # date
    time.sleep(0.5)
    pyautogui.write(formatted_date)
    time.sleep(0.5)
    cord_click(857, 514)
    time.sleep(0.5)
    cord_click(772, 562)  # reason
    time.sleep(0.5)


def main():
    job = pyautogui.prompt(text="", title="Enter the Task", default="Dead Removal")

    #     time.sleep(random.uniform(1, 3))
    cord_click(271, 228)  # click on the search bar
    pyautogui.click()
    time.sleep(2)
    cord_click(290, 377)  # click on constituents updates
    time.sleep(2)
    cord_click(360, 490)  # click on the first constituent
    time.sleep(5)
    cord_click(262, 691)  # interactions
    pyautogui.click()
    time.sleep(4)

    down_command()
    time.sleep(0.5)
    # prompt
    num = pyautogui.prompt(
        text="", title="Enter the number of interactions", default="1"
    )
    pyautogui.click(clicks=2, interval=0.25, duration=1)
    if int(num) == 0:
        print("Quit")
        sys.exit()
    elif int(num) == 1:
        cord_click(420, 748)  # click on first edit
        time.sleep(2.5)
        cord_click(288, 772)  # click on the edit button
        time.sleep(2.5)
        confirm()
    else:
        # click on first edit
        cord_click(420, 748)
        time.sleep(2.5)
        cord_click(288, 772)  # click on the edit button
        time.sleep(2.5)

        # Perform 'decline' and 'confirm' actions based on the value of 'num'
        for _ in range(int(num)):
            decline(int(num))

        confirm()

    # cord_click(1015, 825)  # cancel button
    #  TODO
    cord_click(912, 828)  # save button

    cord_click(286, 546)  # personal info
    time.sleep(1)
    cord_click(529, 646)  # mark

    decease_form()
    cord_click(736, 571)  # save button
    # cord_click(834, 579)  # cancel button

    cord_click(73, 370)  # consituents
    time.sleep(1)
    cord_click(497, 826)  # communications
    time.sleep(1)
    down_command()
    time.sleep(1)
    cord_click(371, 622)  # click on add
    opt_out_form()
    cord_click(271, 228)  # click on the search bar


if __name__ == "__main__":
    threading.Thread(target=keyboard.wait, args=("esc",)).start()
    main()
