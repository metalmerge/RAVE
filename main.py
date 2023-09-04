import random
import threading
import time

import cv2
import keyboard
import numpy as np
import pyautogui
from PIL import Image
from PIL import __version__ as PIL__version__

running = True
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


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


def cord_click_type(x, y, text):
    global running

    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=2, interval=0.25, duration=1)
    pyautogui.typewrite(text)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False
    return True


def cord_click(x, y):
    global running

    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=2, interval=0.25, duration=1)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False


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


def main():
    # screens_to_automate = [0.2, 0.1, 0]
    # channel_name = pyautogui.prompt(
    #     text="", title="Enter the Channel Name", default="Coding 101 with Steve"
    # )
    # for screen_number in screens_to_automate:
    #     if not running:
    #         break

    #     click_on_screen(screen_number)
    #     time.sleep(random.uniform(1, 3))
    cord_click_type(563, 773, "lorem ipsum")
    cord_click(1204, 766)


if __name__ == "__main__":
    threading.Thread(target=keyboard.wait, args=("esc",)).start()
    main()
