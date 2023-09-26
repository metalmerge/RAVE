import pyautogui
import time
import keyboard
from datetime import datetime
from PIL import ImageGrab

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


screenshot = ImageGrab.grab(bbox=(0, 150, round(2880), 900 - 150))
screenshot.show()
