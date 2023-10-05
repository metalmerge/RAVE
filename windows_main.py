# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime
import pyperclip
import keyboard
import pyautogui
from pytesseract import pytesseract

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

x_scale = 1
y_scale = 1
COM_NUM = 1
delay = 0.05
confidence = 0.7
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900
pyautogui.FAILSAFE = True
pyautogui.PAUSE = delay
DEFAULT_PROMPT = "0"
initials = "DE"
noted_date = "1/"
PRIMIS = "windowstarget/receives_imprimis.png"
EDUCATION = "windowstarget/education.png"
LOAD_OPT_OUT_WAIT = "windowstarget/wait_for_load_opt_out.png"
LOAD_OWNER_WAIT = "windowstarget/wait_for_load_owner.png"
PRIMARY_EMAIL = "windowstarget/primary_email.png"
MAX_ATTEMPTS = round(1.25 / (delay * 5))
CURRENT_DATE = datetime.now()
formatted_month = str(CURRENT_DATE.month)
formatted_year = str(CURRENT_DATE.year)
formatted_day = str(CURRENT_DATE.day)

FORMATTED_DATE = f"{formatted_month}/{formatted_year}"
FULL_DATE = f"{formatted_month}/{formatted_day}/{formatted_year}"


def find_and_click_image(image_filename, biasx=0, biasy=0, up_or_down=None):
    global cutOffTopY, delay, MAX_ATTEMPTS, x_scale, y_scale, cutOffBottomY, confidence, PRIMARY_EMAIL
    box = None
    print("Searching for image: " + image_filename)

    if image_filename == "windowstarget/source_file_tab_down.png":
        confidence = 0.8

    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),  # Theoretically this works
            ),
        )
        time.sleep(delay * 5)

        if box is None and up_or_down:
            factor = 14 if up_or_down == "up" else -14
            pyautogui.scroll(factor)
            time.sleep(delay * 2)

    x, y, width, height = box
    x = box.left + width / 2 + biasx
    y = box.top + height / 2 + biasy

    if image_filename not in [
        PRIMIS,
        EDUCATION,
        PRIMARY_EMAIL,
        LOAD_OPT_OUT_WAIT,
        LOAD_OWNER_WAIT,
    ]:
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
    time.sleep(delay)
    find_and_click_image("windowstarget/updates.png")
    if COM_NUM == 2:
        find_and_click_image("windowstarget/third_page.png")
        time.sleep(delay * 20)
    if COM_NUM == 3:
        find_and_click_image("windowstarget/fifth_page.png")
        time.sleep(delay * 20)
    find_and_click_image("windowstarget/name.png", 0, round(25 * y_scale))


def interactions_num_finder():
    global delay
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
                num_index = text.index(pretext) + len(pretext)
                num_text = text[num_index:].strip()
                num = int(extract_digits_from_text(num_text))
                break
            else:
                time.sleep(delay)
                continue
        except ValueError:
            continue
    return num


def click_on_top_interaction(num):
    find_and_click_image(
        "windowstarget/status_alone.png", 0, round(num * 30 * y_scale), "down"
    )
    find_and_click_image("windowstarget/edit_interaction.png", 0, 0, "down")


def interactions_section(num):
    global PRIMIS, LOAD_OWNER_WAIT, PRIMARY_EMAIL
    find_and_click_image("windowstarget/interactions.png")
    click_on_top_interaction(1)
    confirm()
    if num > 1:
        for i in range(2, num + 1):
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            find_and_click_image(LOAD_OWNER_WAIT)
            decline()
    find_and_click_image(PRIMARY_EMAIL, 0, 0, "up")
    find_and_click_image("windowstarget/personal_info.png")
    find_and_click_image("windowstarget/marked_deceased.png")


def confirm():
    global noted_date, initials, FULL_DATE
    find_and_click_image("windowstarget/tab_down_complete.png")
    find_and_click_image("windowstarget/completed_form.png")
    find_and_click_image("windowstarget/wait_for_complete.png")
    tab_command(9, 0)
    keyboard.write(FULL_DATE)
    tab_command(3, 0)
    pyperclip.copy("")
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.1)
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
        find_and_click_image("windowstarget/sites.png")
        tab_command(2, 0)
    if is_text_empty(found_text) is False:
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
    keyboard.write(FULL_DATE)
    tab_command(3, 0)
    pyperclip.copy("")
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.1)
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
        find_and_click_image("windowstarget/sites.png")
        tab_command(2, 0)
    pyautogui.press("down")
    pyautogui.press("enter")
    pyautogui.press("enter")
    keyboard.write("Note: Duplicate - " + initials)
    tab_command(2, 0)
    pyautogui.press("enter")


def deceased_form():
    global noted_date, FORMATTED_DATE
    find_and_click_image("windowstarget/deceased_date.png")
    if noted_date == "1/":
        keyboard.write(FORMATTED_DATE)
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
    global FULL_DATE
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
    time.sleep(delay)
    pyautogui.press("tab")
    keyboard.write(FULL_DATE)
    time.sleep(delay)
    tab_command(3, 0)
    # find_and_click_image("windowstarget/source_file_tab_down.png")
    keyboard.write("Deceased")
    find_and_click_image("windowstarget/double_deceased.png")
    pyautogui.press("enter")


def end_time_recording(start_time):
    global FULL_DATE
    end_time = time.time()
    duration = end_time - start_time
    log_file = "time_logs/windows_program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    # find the top y coordinate of the image on the screen
    global delay, MAX_ATTEMPTS, x_scale, y_scale, confidence
    box = None
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(delay * 5)
        print("Searching for image: " + image_filename)

    _, y, width, height = box

    image_cords_x = (box.left) + width / 2
    image_cords_y = (box.top) + height / 2

    return round(y), (image_cords_x, image_cords_y)


def main():
    global initials, cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, EDUCATION, COM_NUM, delay, PRIMARY_EMAIL
    input_str = pyautogui.prompt(
        text="Enter Initials, which computer number this is, and delay time -1 to quit",
        title="Enter Initials, which computer number this is, and delay time -1 to quit",
        default="DE, 1, 0.05",
    )
    initials, computer_number, delay = input_str.strip().split(",")
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    delay = float(delay.strip())
    COM_NUM = int(computer_number.strip())
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("windowstarget/blackbaud_CRM.png")

    while initials != "-1":
        confirm()
        # start_time = time.time()
        # get_to_dead_page()
        # num = interactions_num_finder()

        # interactions_section(num)
        # deceased_form()
        # move_to_communications()
        # opt_out_form()

        # end_time_recording(start_time)
        # find_and_click_image(PRIMARY_EMAIL)  # TODO find a way to remove
        break


if __name__ == "__main__":
    main()
