import pyautogui
import time
import keyboard
from datetime import datetime

pyautogui.FAILSAFE = True
DELAY = 1
pyautogui.PAUSE = DELAY


def down_command(num):
    for _ in range(0, num):
        pyautogui.press("down")


def find_and_click_image(image_filename, biasx, biasy):
    try:
        box = None
        x_scale = 1440 / 2880
        y_scale = 900 / 1800
        while box is None:
            box = pyautogui.locateOnScreen(image_filename, confidence=0.9)
            time.sleep(DELAY)
            print("Searching for image: " + image_filename)

        x, y, width, height = box

        # screenshot = pyautogui.screenshot()
        # found_image_screenshot = screenshot.crop((x, y, x + width, y + height))
        # found_image_screenshot.show()
        # found_image_screenshot.save(image_filename)

        x = box.left * x_scale
        y = box.top * y_scale

        cord_click(x + width / 4 + biasx, y + height / 4 + biasy)
        # print(x + width / 4 + biasx, y + height / 4 + biasy)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def cord_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


global full_date
find_and_click_image("target/solicit_code.png", 0, 0)
keyboard.write("Imprimis")
find_and_click_image("target/opt_out_comments.png", 0, 0)
find_and_click_image("target/start_date.png", 0, 0)
# find_and_click_image("target/today.png", 0, 0)
keyboard.write("9/23/2023")
find_and_click_image("target/prefernce_tab_down.png", 0, 0)
find_and_click_image("target/opt_out.png", 0, 0)
find_and_click_image("target/imprintis_source.png", 0, 0)
keyboard.write("Deceased")
find_and_click_image("target/source_evidence.png", 0, 0)
down_command(3)
# find_and_click_image("target/save.png", 0, 0)
find_and_click_image("target/cancel.png", 0, 0)  # cancel button
