import time
import pyautogui
import threading
import keyboard  # Added library for detecting keyboard input

# Global variable to control the loop
running = True


def click_on_screen(screen_number):
    global running  # Access the global variable

    # Load the screenshot
    screenshot_path = f"screenshots/screen{screen_number}.png"
    target_location = pyautogui.locateOnScreen(screenshot_path)

    if target_location is None:
        print(f"Screenshot {screen_number} not found on the screen.")
        return

    # Get the center of the target location
    target_x, target_y, target_width, target_height = target_location
    target_center_x = target_x + target_width // 2
    target_center_y = target_y + target_height // 2

    # Move the mouse to the target location and click
    pyautogui.moveTo(target_center_x, target_center_y)
    pyautogui.click()

    # Check if the user pressed the escape key
    if keyboard.is_pressed("esc"):
        print("Escape key pressed. Stopping the program.")
        running = False


def main():
    # List of screen numbers to automate (adjust as needed)
    screens_to_automate = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for screen_number in screens_to_automate:
        if not running:
            break  # Exit the loop if escape key is pressed

        click_on_screen(screen_number)
        time.sleep(2)  # Add a delay to ensure the action is performed


if __name__ == "__main__":
    # Start a separate thread to detect the escape key
    threading.Thread(target=keyboard.wait, args=("esc",)).start()
    main()
