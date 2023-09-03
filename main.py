import time
import random
import pyautogui
import threading
import keyboard
from PIL import __version__ as PIL__version__

running = True
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
channel_name = pyautogui.prompt(
    text="", title="Enter the Channel Name", default="Coding 101 with Steve"
)


def click_on_screen(screen_number):
    global running

    screenshot_path = f"/Users/dimaermakov/Downloads/target/screen{screen_number}.png"

    target_location = pyautogui.locateOnScreen(screenshot_path, confidence=0.9)

    if target_location is None:
        print(f"Screenshot {screen_number} not found on the screen.")
        return

    target_x, target_y, target_width, target_height = target_location
    target_center_x = target_x + target_width // 2
    target_center_y = target_y + target_height // 2
    pyautogui.moveTo(target_center_x, target_center_y)
    pyautogui.click(duration=0.25)

    # if screen_number == 3:
    #     input_text = "Sample Input"
    #     pyautogui.typewrite(input_text)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False


def main():
    screens_to_automate = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for screen_number in screens_to_automate:
        if not running:
            break

        click_on_screen(screen_number)
        time.sleep(random.uniform(3, 5))


if __name__ == "__main__":
    threading.Thread(target=keyboard.wait, args=("esc",)).start()
    main()
