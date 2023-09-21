import pyautogui
import time


def find_and_click_image(image_filename, biasx, biasy):
    time.sleep(1)
    try:
        # screenshot = pyautogui.screenshot()
        box = None
        while box is None:
            box = pyautogui.locateOnScreen(image_filename, confidence=0.8)
            time.sleep(0.5)

        # Calculate the scaling factors
        x_scale = 1500 / 2880
        y_scale = 900 / 1777

        # print(box)
        x, y, width, height = box

        # found_image_screenshot = screenshot.crop((x, y, x + width, y + height))
        # found_image_screenshot.save("found_image.png")
        # found_image_screenshot.show()

        x = box.left * x_scale
        y = box.top * y_scale

        cord_click(x + width / 4 + biasx, y + height / 4 + biasy)
        # print(x + width / 4 + biasx, y + height / 4 + biasy)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# 1500, 900


def cord_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


find_and_click_image("test.png", 0, 0)
