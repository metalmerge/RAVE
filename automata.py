import pyautogui
import pyperclip
import time
import keyboard
from datetime import datetime
from PIL import ImageGrab
import os

DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
PRIMIS = "target/receives_imprimis.png"
DELAY = 0.1
MAX_ATTEMPTS = round(1.25 / (DELAY * 5))
x_scale = 1
y_scale = 1
pyautogui.FAILSAFE = True
pyautogui.PAUSE = DELAY
current_date = datetime.now()
formatted_date = current_date.strftime("%-m/%Y")
full_date = current_date.strftime("%-m/%-d/%Y")
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900


def is_text_empty(text):
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False


def down_command(num):
    for _ in range(0, num):
        pyautogui.press("down")


def find_and_click_image(image_filename, biasx, biasy):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY
    box = None
    attempts = 0
    print("Searching for image: " + image_filename)
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=0.9,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),  # theocratically this works
            ),
        )
        time.sleep(DELAY * 5)
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            if os.name == "posix":  # macOS
                os.system(
                    f'osascript -e \'display notification "Could not find image {image_filename}" with title "Error"\''
                )
            elif os.name == "nt":  # Windows
                os.system(
                    f'powershell -command "New-BurntToastNotification -Text "Could not find image {image_filename}" -AppLogo '
                    + '"'
                    + os.getcwd()
                    + "/target/primis.png"
                    + ")"
                    + '"'
                )
            else:
                print("Unsupported operating system")
            break

    x, y, width, height = box
    x = box.left / 2 + width / 4 + biasx
    y = box.top / 2 + height / 4 + biasy
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != "target/education.png"
        and image_filename != "target/receives_imprimis.png"
        and image_filename != "target/wait_for_load_opt_out.png"
        and image_filename != "target/wait_for_owner.png"
    ):
        cord_click((x, y))


def cord_click(cords):
    pyautogui.moveTo(cords[0], cords[1])
    pyautogui.click()


def copy_clipboard():
    pyperclip.copy("")  # <- This prevents last copy replacing current copy of null.
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("c")
    pyautogui.keyUp("c")
    pyautogui.keyUp("ctrl")
    time.sleep(0.1)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()


def tab_command(num, delay):
    for _ in range(0, num):
        time.sleep(delay)
        pyautogui.press("tab")


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


find_and_click_image("target/tab_down_complete.png", 0, 0)
find_and_click_image("target/completed_form.png", 0, 0)
find_and_click_image("target/wait_for_complete.png", 0, 0)
tab_command(7, 0)
keyboard.write(full_date)
tab_command(3, 0)
keyboard.press("command+A")
keyboard.press_and_release("command+C")
found_text = pyperclip.paste()
print(found_text)


pyautogui.press("down")
pyautogui.press("enter")
pyautogui.press("enter")
keyboard.write("Note: Not Researched - " + initials)
tab_command(2, 0)
