# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime
import pyperclip
import keyboard
import pyautogui
from pytesseract import pytesseract
import os

# Interactions: 2 = 79.14 bot; 75.66 no copy pasting, experienced, fast as possible human
# Interactions: 1 = 33.86 bot; 45.68 human

# TODO
# Protential improvements:
#   - Find a better way to know the number of interactions than using extract_text_from_coordinates
#   - Working sound notification for macOS and Windows
#   - Use mss to take screenshots instead of pyautogui
#   - Find workaround to recieves imprints and waits
#   - Figure out how to extract the date from the comments
#   - Figure out how to use the copy paste for confirm and decline

# original_x_scale = 1440 / 2880
# original_y_scale = 900 / 1800
# make sure commands and control are accounted for based on type of computer

DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
PRIMIS = "windowstarget/receives_imprimis.png"
EDUCATION = "windowstarget/education.png"
LOAD_OPT_OUT_WAIT = "windowstarget/wait_for_load_opt_out.png"
LOAD_OWNER_WAIT = "windowstarget/wait_for_load_owner.png"
DELAY = 0.05
MAX_ATTEMPTS = round(1.25 / (DELAY * 5))
x_scale = 1
y_scale = 1
COM_NUM = 1
CONFIDENCE = 0.7
pyautogui.FAILSAFE = True
pyautogui.PAUSE = DELAY
current_date = datetime.now()

formatted_date = current_date.strftime("%m/%Y")
full_date = current_date.strftime("%m/%d/%Y")

CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900


def find_and_click_image_with_search(image_filename, biasx, biasy, up_or_down):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, CONFIDENCE
    box = None
    print("Searching for image: " + image_filename)
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=CONFIDENCE,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),  # theocratically this works
            ),
        )
        time.sleep(DELAY * 10)
        if box is None:
            factor = -14
            if up_or_down == "up":
                factor = 14
            pyautogui.scroll(factor)
            time.sleep(DELAY * 2)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != EDUCATION
        and image_filename != "windowstarget/primary_email.png"
        and image_filename != LOAD_OPT_OUT_WAIT
        and image_filename != LOAD_OWNER_WAIT
    ):
        cord_click((x, y))


def find_and_click_image_with_bias(image_filename, biasx, biasy):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, CONFIDENCE
    box = None
    print("Searching for image: " + image_filename)
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=CONFIDENCE,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),  # theocratically this works
            ),
        )
        time.sleep(DELAY * 5)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != EDUCATION
        and image_filename != "windowstarget/primary_email.png"
        and image_filename != LOAD_OPT_OUT_WAIT
        and image_filename != LOAD_OWNER_WAIT
    ):
        cord_click((x, y))


def find_and_click_image(image_filename):
    global cutOffTopY, DELAY, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, CONFIDENCE
    box = None

    print("Searching for image: " + image_filename)
    if (image_filename == "windowstarget/source_file_tab_down.png"):
        CONFIDENCE = .8
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=CONFIDENCE,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),  # theocratically this works
            ),
        )
        time.sleep(DELAY * 5)

    x, y, width, height = box
    x = box.left + width / 2
    y = box.top + height / 2
    if (  # TODO find a way to remove
        image_filename != PRIMIS
        and image_filename != EDUCATION
        and image_filename != LOAD_OPT_OUT_WAIT
        and image_filename != "windowstarget/primary_email.png"
        and image_filename != LOAD_OWNER_WAIT
    ):
        cord_click((x, y))


def extract_text_from_coordinates(x1, y1, x2, y2):
    path_to_tesseract = r"C:\Users\dermakov\Downloads\RAVE-main\RAVE-main\tesseract.exe"
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
    find_and_click_image("windowstarget/constituents.png")
    find_and_click_image("windowstarget/updates.png")
    if COM_NUM == 2:  # untested
        find_and_click_image("windowstarget/third_page.png")
    if COM_NUM == 3:
        find_and_click_image("windowstarget/fifth_page.png")
    find_and_click_image_with_bias("windowstarget/name.png", 0, round(25 * y_scale))


def interactions_num_finder():
    global DELAY
    while True:
        pretext = "Interactions: "
        try:
            text = extract_text_from_coordinates(
                1192,
                500,
                1286,
                524,
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
        "windowstarget/status_alone.png", 0, round(num * 30 * y_scale), "down"
    )
    # time.sleep(1)
    find_and_click_image_with_search("windowstarget/edit_interaction.png", 0, 0, "down")


def interactions_section(num):
    global PRIMIS, LOAD_OWNER_WAIT
    find_and_click_image("windowstarget/interactions.png")
    click_on_top_interaction(1)
    confirm()
    if num > 1:  # untested
        for i in range(2, num+1):
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            find_and_click_image(LOAD_OWNER_WAIT)
            decline()
    # time.sleep(2)
    find_and_click_image_with_search("windowstarget/primary_email.png", 0, 0, "up")
    find_and_click_image("windowstarget/personal_info.png")
    find_and_click_image("windowstarget/marked_deceased.png")


def confirm():
    global noted_date, initials, full_date

    find_and_click_image("windowstarget/tab_down_complete.png")
    find_and_click_image("windowstarget/completed_form.png")
    find_and_click_image("windowstarget/wait_for_complete.png")
    tab_command(9, 0)
    keyboard.write(full_date)
    # pyperclip.copy("")
    tab_command(3, 0)
    # keyboard.press("ctrl+a")
    # time.sleep(0.2)
    # keyboard.press("ctrl+c")
    # keyboard.write("Note: Confirmed - " + initials)
    # keyboard.press("ctrl+v")
    # found_text = pyperclip.paste()
    time.sleep(DELAY)
    found_text = extract_text_from_coordinates(601, 600, 1277, 726)
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
        find_and_click_image("windowstarget/sites.png")
        tab_command(2,0)
    if is_text_empty(found_text) == False:
        pyautogui.press("down")
        pyautogui.press("enter")
        pyautogui.press("enter")
    keyboard.write("Note: Not Researched - " + initials)
    tab_command(2, 0)
    pyautogui.press("enter")


def decline():
    global initials, CRM_cords, noted_date
    find_and_click_image("windowstarget/tab_down_complete.png")
    find_and_click_image("windowstarget/declined.png")
    find_and_click_image("windowstarget/wait_for_declined.png")
    tab_command(8, 0)
    keyboard.write(full_date)
    # pyperclip.copy("")
    tab_command(3, 0)
    # keyboard.press("command+A")
    # time.sleep(0.1)
    # keyboard.press_and_release("command+C")
    # found_text = pyperclip.paste()
    time.sleep(DELAY)
    found_text = extract_text_from_coordinates(601, 600, 1277, 726)
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
        find_and_click_image("windowstarget/sites.png")
        tab_command(2, 0)
    pyautogui.press("down")
    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - " + initials)
    tab_command(2, 0)
    pyautogui.press("enter")


def deceased_form():
    global noted_date, formatted_date
    find_and_click_image("windowstarget/deceased_date.png")
    if noted_date == "1/":
        keyboard.write(formatted_date)
    elif noted_date != "1/":
        keyboard.write(noted_date)
        noted_date = "1/"
    find_and_click_image("windowstarget/source_tab_down.png")
    find_and_click_image("windowstarget/communication_from.png")
    pyautogui.press("enter")


def move_to_communications():
    global PRIMIS
    find_and_click_image("windowstarget/constitute.png")
    find_and_click_image(PRIMIS)  # TODO find a way to remove
    find_and_click_image("windowstarget/communications.png")
    find_and_click_image("windowstarget/add.png")


def opt_out_form():
    global full_date
    find_and_click_image("windowstarget/solicit_code.png")
    keyboard.write("Imprimis")
    find_and_click_image("windowstarget/imprimis_three.png")
    find_and_click_image("windowstarget/imprimis_done.png")
    pyautogui.press("tab")
    pyautogui.press("tab")
    for _ in range(0, 11):
        pyautogui.press("backspace")
    keyboard.write("Opt-out")
    find_and_click_image("windowstarget/opt_out.png")
    pyautogui.press("tab")
    keyboard.write(full_date)
    find_and_click_image("windowstarget/source_file_tab_down.png")
    # tab_command(3,0)
    # keyboard.write("Deceased")
    find_and_click_image("windowstarget/double_deceased.png")
    # tab_command(5,0)
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
    global DELAY, MAX_ATTEMPTS, x_scale, y_scale, CONFIDENCE
    box = None
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=CONFIDENCE,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(DELAY * 5)
        print("Searching for image: " + image_filename)

    _, y, width, height = box

    image_cords_x = (box.left) + width / 2
    image_cords_y = (box.top) + height / 2

    return round(y), (image_cords_x, image_cords_y)


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
    y_scale = screen_height / 900
    COM_NUM = int(computer_number.strip())
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowstarget/blackbaud_CRM.png")

    while initials != "-1":
        start_time = time.time()
        get_to_dead_page()
        num = interactions_num_finder()
        
        interactions_section(num)
        deceased_form()
        move_to_communications()
        opt_out_form()

        end_time_recording(start_time)
        find_and_click_image("windowstarget/primary_email.png")  # TODO find a way to remove

if __name__ == "__main__":
    main()
