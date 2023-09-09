import time
import pyautogui
from PIL import Image


def click_on_image(image_path):
    try:
        # Load the image
        image = Image.open(image_path)

        # Get the screen width and height
        screen_width, screen_height = pyautogui.size()

        # Search for the image on the screen
        for x in range(0, screen_width, 10):
            for y in range(0, screen_height, 10):
                screen_shot = pyautogui.screenshot(
                    region=(x, y, image.width, image.height)
                )
                if screen_shot.getbbox() is not None:
                    if screen_shot == image:
                        # Calculate the coordinates of the image's center
                        image_location = (x + image.width / 2, y + image.height / 2)

                        # Move the mouse to the center of the image and click
                        pyautogui.moveTo(image_location)
                        pyautogui.click()

                        return True

        print(f"Image '{image_path}' not found on the screen.")
        return False

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


# Example usage


pyautogui.prompt()
pyautogui.click(600, 600)
time.sleep(1)
# click_on_image("target/1.png")
click_on_image("target/whole.png")
time.sleep(1)
# pyautogui.press("enter")
# pyautogui.write(r"Note: Not Researched - DE", interval=0.1)
