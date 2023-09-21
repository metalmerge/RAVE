import sys

import keyboard
import pyautogui


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


def cord_click_type(x, y, text):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.typewrite(text)

    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        sys.exit()
    return True


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


def contains_numbers(text):
    return any(char.isdigit() for char in text)


def find_year(text):
    # Define a regular expression pattern to match a year (e.g., 4 digits)
    pattern = r"\b\d{4}\b"
    match = re.search(pattern, text)
    if match:
        year = match.group()
        return year
    else:
        return None


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
        running = False
        sys.exit()