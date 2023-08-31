import time
import random
import pyautogui
import threading
import keyboard

running = True


def click_on_screen(screen_number):
    global running

    screenshot_path = f"screenshots/screen{screen_number}.png"
    target_location = pyautogui.locateOnScreen(screenshot_path)

    if target_location is None:
        print(f"Screenshot {screen_number} not found on the screen.")
        return

    target_x, target_y, target_width, target_height = target_location
    target_center_x = target_x + target_width // 2
    target_center_y = target_y + target_height // 2

    # Move the mouse to the target location and click
    pyautogui.moveTo(target_center_x, target_center_y)
    pyautogui.click()

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
