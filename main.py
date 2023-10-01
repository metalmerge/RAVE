# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime
import pyperclip
import keyboard
import pyautogui
import pytesseract
import os

# Interactions: 2 = 79.14 bot; 75.66 no copy pasting, experienced, fast as possible human
# Interactions: 1 = 50.66 bot; 51.08 no copy pasting, experienced, fast as possible human

# TODO
# Protential improvements:
#   - Find a better way to know the number of interactions than using extract_text_from_coordinates
#   - Working sound notification for macOS and Windows
#   - Use mss to take screenshots instead of pyautogui
#   - Find workaround to recieves imprints and waits
#   - Figure out how to extract the date from the comments

# original_x_scale = 1440 / 2880
# original_y_scale = 900 / 1800
# make sure commands and control are accounted for based on type of computer

# TODO rework readme

DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
PRIMIS = "target/receives_imprimis.png"
EDUCATION = "target/education.png"
LOAD_OPT_OUT_WAIT = "target/wait_for_load_opt_out.png"
LOAD_OWNER_WAIT = "target/wait_for_load_owner.png"
DELAY = 0.01
MAX_ATTEMPTS = round(1.25 / (DELAY * 5))
x_scale = 1
y_scale = 1
COM_NUM = 1
pyautogui.FAILSAFE = True
pyautogui.PAUSE = DELAY
current_date = datetime.now()


if os.name == "posix":
    formatted_date = current_date.strftime("%-m/%Y")
    full_date = current_date.strftime("%-m/%-d/%Y")
else:
    formatted_date = current_date.strftime("%m/%Y")
    full_date = current_date.strftime("%m/%d/%Y")

CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900


def find_and_click_image_with_search(image_filename, biasx, biasy, up_or_down):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY
    box = None
    # print("Searching for image: " + image_filename)
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
        if box is None:
            pyautogui.press(up_or_down)
            pyautogui.press(up_or_down)
            pyautogui.press(up_or_down)
            time.sleep(DELAY * 5)

    x, y, width, height = box
    x = box.left / 2 + width / 4 + biasx
    y = box.top / 2 + height / 4 + biasy
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != EDUCATION
        and image_filename != LOAD_OPT_OUT_WAIT
        and image_filename != LOAD_OWNER_WAIT
    ):
        cord_click((x, y))


def find_and_click_image_with_bias(image_filename, biasx, biasy):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY
    box = None
    attempts = 0
    # print("Searching for image: " + image_filename)
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
            if os.name == "posix":  # macOS # TODO untested
                os.system(
                    f'osascript -e \'display notification "Could not find image {image_filename}" with title "Error" sound name "Glass"\''
                )
        elif os.name == "nt":  # Windows # TODO untested
            os.system(
                f'powershell -command "New-BurntToastNotification -Text "Could not find image {image_filename}" -AppLogo '
                + '"'
                + os.getcwd()
                + "/target/chrome.png"
                + ")"
                + '"'
            )

    x, y, width, height = box
    x = box.left / 2 + width / 4 + biasx
    y = box.top / 2 + height / 4 + biasy
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != EDUCATION
        and image_filename != LOAD_OPT_OUT_WAIT
        and image_filename != LOAD_OWNER_WAIT
    ):
        cord_click((x, y))


def find_and_click_image(image_filename):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY
    box = None
    attempts = 0
    # print("Searching for image: " + image_filename)
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
            if os.name == "posix":  # macOS # TODO untested
                os.system(
                    f'osascript -e \'display notification "Could not find image {image_filename}" with title "Error" sound name "Glass"\''
                )
        elif os.name == "nt":  # Windows # TODO untested
            os.system(
                f'powershell -command "New-BurntToastNotification -Text "Could not find image {image_filename}" -AppLogo '
                + '"'
                + os.getcwd()
                + "/target/chrome.png"
                + ")"
                + '"'
            )

    x, y, width, height = box
    x = box.left / 2 + width / 4
    y = box.top / 2 + height / 4
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != EDUCATION
        and image_filename != LOAD_OPT_OUT_WAIT
        and image_filename != LOAD_OWNER_WAIT
    ):
        cord_click((x, y))


def extract_text_from_coordinates(x1, y1, x2, y2):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    screenshot = pyautogui.screenshot()
    textbox_image = screenshot.crop((x1, y1, x2, y2))
    extracted_text = pytesseract.image_to_string(textbox_image)
    # print(extracted_text.strip())
    return extracted_text.strip()


def cord_click(cords):
    pyautogui.moveTo(cords[0], cords[1])
    pyautogui.click()


def tab_command(num, delay):
    for _ in range(0, num):
        time.sleep(delay)
        pyautogui.press("tab")


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


def is_text_empty(text):
    if text is None or len(text.strip()) == 0:
        return True
    else:
        return False


def get_to_dead_page():
    global COM_NUM
    find_and_click_image("target/constituents.png")
    find_and_click_image("target/updates.png")
    if COM_NUM == 2:  # untested
        find_and_click_image("target/third_page.png")
    if COM_NUM == 3:
        find_and_click_image("target/fifth_page.png")
    find_and_click_image_with_bias("target/name.png", 0, round(25 * y_scale))


def interactions_num_finder():
    global DELAY
    while True:
        pretext = "Interactions: "
        try:
            text = extract_text_from_coordinates(
                round(420 * x_scale),
                round(1350 * y_scale),
                round(620 * x_scale),
                round(1400 * y_scale),
            )
            if pretext in text:
                # Extract the number following "Interactions:"
                num_index = text.index(pretext) + len(pretext)
                num_text = text[num_index:].strip()
                num = int(extract_digits_from_text(num_text))
                break
            else:
                time.sleep(DELAY)
                continue
        except ValueError:
            continue
    return num


def click_on_top_interaction(num):
    find_and_click_image_with_search(
        "target/status_alone.png", 0, round(num * 30 * y_scale), "down"
    )
    find_and_click_image_with_search("target/edit_interaction.png", 0, 0, "down")


def interactions_section(num):
    global PRIMIS, LOAD_OWNER_WAIT
    find_and_click_image("target/interactions.png")
    click_on_top_interaction(1)
    confirm()
    if num > 1:  # untested
        for i in range(2, num):
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            decline()
    find_and_click_image(PRIMIS)
    find_and_click_image_with_search("target/personal_info.png", 0, 0, "up")
    find_and_click_image("target/marked_deceased.png")


def confirm():
    global noted_date, initials, full_date

    find_and_click_image("target/tab_down_complete.png")
    find_and_click_image("target/completed_form.png")
    find_and_click_image("target/wait_for_complete.png")
    tab_command(7, 0)
    keyboard.write(full_date)
    pyperclip.copy("")
    tab_command(3, 0)
    keyboard.press("command+A")
    time.sleep(0.1)
    keyboard.press_and_release("command+C")
    found_text = pyperclip.paste()
    if (
        (
            extract_digits_from_text(found_text) != ""
            or "year" in found_text
            or "month" in found_text
            or "January" in found_text
            or "February" in found_text
            or "March" in found_text
            or "April" in found_text
            or "May" in found_text
            or "June" in found_text
            or "July" in found_text
            or "August" in found_text
            or "September" in found_text
            or "October" in found_text
            or "November" in found_text
            or "December" in found_text
        )
        and "id=" not in found_text
        and "batch" not in found_text
    ):
        noted_date = pyautogui.prompt(text="", title="Noted Date?", default="1/")
        find_and_click_image("target/sites.png")
    if is_text_empty(found_text) == False:
        pyautogui.press("down")
        pyautogui.press("enter")
        pyautogui.press("enter")
    keyboard.write("Note: Not Researched - " + initials)
    tab_command(2, 0)
    pyautogui.press("enter")


def decline():
    global initials, CRM_cords, noted_date
    find_and_click_image("target/tab_down_complete.png")
    find_and_click_image("target/declined.png")
    tab_command(7, 0)
    keyboard.write(full_date)
    pyperclip.copy("")
    tab_command(3, 0)
    keyboard.press("command+A")
    time.sleep(0.1)
    keyboard.press_and_release("command+C")
    found_text = pyperclip.paste()
    if (
        (
            extract_digits_from_text(found_text) != ""
            or "year" in found_text
            or "month" in found_text
            or "January" in found_text
            or "February" in found_text
            or "March" in found_text
            or "April" in found_text
            or "May" in found_text
            or "June" in found_text
            or "July" in found_text
            or "August" in found_text
            or "September" in found_text
            or "October" in found_text
            or "November" in found_text
            or "December" in found_text
        )
        and "id=" not in found_text
        and "batch" not in found_text
    ):
        noted_date = pyautogui.prompt(text="", title="Noted Date?", default="1/")
        find_and_click_image("target/sites.png")
    pyautogui.press("down")
    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - " + initials)
    tab_command(2, 0)
    pyautogui.press("enter")


def deceased_form():
    global noted_date, formatted_date
    find_and_click_image("target/deceased_date.png")
    if noted_date == "1/":
        keyboard.write(formatted_date)
    elif noted_date != "1/":
        keyboard.write(noted_date)
        noted_date = "1/"
    find_and_click_image("target/source_tab_down.png")
    find_and_click_image("target/communication_from.png")
    pyautogui.press("enter")


def move_to_communications():
    global PRIMIS
    find_and_click_image("target/constitute.png")
    find_and_click_image(PRIMIS)  # TODO find a way to remove
    find_and_click_image("target/communications.png")
    find_and_click_image_with_search("target/add.png", 0, 0, "down")


def opt_out_form():
    global full_date
    find_and_click_image("target/solicit_code.png")
    keyboard.write("Imprimis")
    find_and_click_image("target/imprimis_three.png")
    find_and_click_image("target/imprintis_done.png")
    pyautogui.press("tab")
    for _ in range(0, 11):
        pyautogui.press("backspace")
    keyboard.write("Opt-out")
    find_and_click_image("target/opt_out.png")
    pyautogui.press("tab")
    keyboard.write(full_date)
    find_and_click_image("target/source_file_tab_down.png")
    find_and_click_image("target/double_deceased.png")
    pyautogui.press("enter")


def end_time_recording(start_time):
    global full_date
    end_time = time.time()
    duration = end_time - start_time
    log_file = "program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    # find the top y coordinate of the image on the screen
    global DELAY, MAX_ATTEMPTS, x_scale, y_scale
    box = None
    attempts = 0
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=0.9,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(DELAY * 5)
        # print("Searching for image: " + image_filename)
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
                    + "/target/chrome.png"
                    + ")"
                    + '"'
                )
            else:
                print("Unsupported operating system")
            break

    _, y, width, height = box
    image_cords_x = box.left / 2 + width / 4
    image_cords_y = box.top / 2 + height / 4

    return round(y / 2), (image_cords_x, image_cords_y)


def main():
    global initials, cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, EDUCATION, COM_NUM
    input_str = pyautogui.prompt(
        text="Enter Initials and which computer number this is, -1 to quit",
        title="Enter Initials and which computer number this is, -1 to quit",
        default="DE, 1",
    )
    initials, computer_number = input_str.strip().split(",")
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height
    COM_NUM = int(computer_number.strip())
    cutOffBottomY = y_scale
    y_scale /= 900
    cutOffTopY, CRM_cords = cutoff_section_of_screen("target/blackbaud_CRM.png")
    # cutOffBottomY, _ = cutoff_section_of_screen("target/chrome.png")
    cord_click(CRM_cords)

    while initials != "-1":
        start_time = time.time()

        get_to_dead_page()
        num = interactions_num_finder()
        interactions_section(num)
        deceased_form()
        move_to_communications()
        opt_out_form()

        end_time_recording(start_time)
        find_and_click_image(EDUCATION)  # TODO find a way to remove


if __name__ == "__main__":
    main()
