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

initials = "DE"
noted_date = "1/"
delay = 0.01
x_scale = 1
y_scale = 1
COM_NUM = 1
confidence = 0.9
CRM_cords = (0, 0)
cutOffTopY = 0
cutOffBottomY = 900
pyautogui.FAILSAFE = True
pyautogui.PAUSE = delay
CURRENT_DATE = datetime.now()
FORMATTED_DATE = CURRENT_DATE.strftime("%-m/%Y")
FULL_DATE = CURRENT_DATE.strftime("%-m/%-d/%Y")
DEFAULT_PROMPT = "0"
PRIMIS = "appletarget/receives_imprimis.png"
EDUCATION = "appletarget/education.png"
LOAD_OPT_OUT_WAIT = "appletarget/wait_for_load_opt_out.png"
LOAD_OWNER_WAIT = "appletarget/wait_for_load_owner.png"
MAX_ATTEMPTS = round(1.25 / (delay * 5))


def find_and_click_image(image_filename, biasx=0, biasy=0, up_or_down=None):
    box = None
    attempts = 0
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(
                0,
                cutOffTopY,
                round(2880 * x_scale),
                round(cutOffBottomY * 2 * y_scale),
            ),
        )
        time.sleep(delay * 5)
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            os.system(
                f'osascript -e \'display notification "Could not find image {image_filename}" with title "Error" sound name "Glass"\''
            )
        if box is None and up_or_down is not None:
            pyautogui.press(up_or_down)
            pyautogui.press(up_or_down)
            pyautogui.press(up_or_down)
            time.sleep(delay * 5)
    x, y, width, height = box
    x = box.left / 2 + width / 4 + biasx
    y = box.top / 2 + height / 4 + biasy

    if image_filename not in [
        PRIMIS,
        EDUCATION,
        LOAD_OPT_OUT_WAIT,
        LOAD_OWNER_WAIT,
    ]:
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


def tab_command(number_of_interactions):
    for _ in range(0, number_of_interactions):
        pyautogui.press("tab")


def extract_digits_from_text(text):
    return "".join(filter(str.isdigit, text))


def is_text_empty(text):
    if text is None or len(text.strip()) == 0:
        return True
    return False


def get_to_dead_page():
    global COM_NUM
    find_and_click_image("appletarget/constituents.png")
    find_and_click_image("appletarget/updates.png")
    if COM_NUM == 2:  # TODO untested
        find_and_click_image("appletarget/third_page.png")
    if COM_NUM == 3:
        find_and_click_image("appletarget/fifth_page.png")
    find_and_click_image("appletarget/name.png", 0, round(25 * y_scale))


def interactions_num_finder():
    global delay
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
                number_of_interactions = int(extract_digits_from_text(num_text))
                break
            else:
                time.sleep(delay)
                continue
        except ValueError:
            continue
    return number_of_interactions


def click_on_top_interaction(number_of_interactions):
    find_and_click_image(
        "appletarget/status_alone.png",
        0,
        round(number_of_interactions * 30 * y_scale),
        "down",
    )
    find_and_click_image("appletarget/edit_interaction.png", 0, 0, "down")


def interactions_section(number_of_interactions):
    global PRIMIS, LOAD_OWNER_WAIT
    find_and_click_image("appletarget/interactions.png")
    click_on_top_interaction(1)
    process_application()
    if number_of_interactions > 1:  # untested
        for i in range(2, number_of_interactions):
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            process_application(False)
    find_and_click_image(PRIMIS, 0, 0, "up")
    find_and_click_image("appletarget/personal_info.png")
    find_and_click_image("appletarget/marked_deceased.png")


def process_application(is_confirmed=True):
    global noted_date, initials, FULL_DATE, CRM_cords

    find_and_click_image("appletarget/tab_down_complete.png")
    if is_confirmed:
        find_and_click_image("appletarget/completed_form.png")
        find_and_click_image("appletarget/wait_for_complete.png")
    else:
        find_and_click_image("appletarget/declined.png")
        find_and_click_image("appletarget/wait_for_decline.png")

    tab_command(7)
    keyboard.write(FULL_DATE)
    pyperclip.copy("")
    tab_command(3)
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
        find_and_click_image("appletarget/sites.png")

    pyautogui.press("down")
    pyautogui.press("enter")
    pyautogui.press("enter")

    if is_confirmed:
        keyboard.write("Note: Not Researched - " + initials)
    else:
        keyboard.write("Note: Duplicate - " + initials)

    tab_command(2)
    pyautogui.press("enter")


def deceased_form():
    global noted_date, FORMATTED_DATE
    find_and_click_image("appletarget/deceased_date.png")
    if noted_date == "1/":
        keyboard.write(FORMATTED_DATE)
    elif noted_date != "1/":
        keyboard.write(noted_date)
        noted_date = "1/"
    find_and_click_image("appletarget/source_tab_down.png")
    find_and_click_image("appletarget/communication_from.png")
    pyautogui.press("enter")


def move_to_communications():
    global PRIMIS
    find_and_click_image("appletarget/constitute.png")
    find_and_click_image(PRIMIS)  # TODO find a way to remove
    find_and_click_image("appletarget/communications.png")
    find_and_click_image("appletarget/add.png", 0, 0, "down")


def opt_out_form():
    global FULL_DATE
    find_and_click_image("appletarget/solicit_code.png")
    keyboard.write("Imprimis")
    find_and_click_image("appletarget/imprimis_three.png")
    find_and_click_image("appletarget/imprimis_done.png")
    pyautogui.press("tab")
    for _ in range(0, 11):
        pyautogui.press("backspace")
    keyboard.write("Opt-out")
    find_and_click_image("appletarget/opt_out.png")
    pyautogui.press("tab")
    keyboard.write(FULL_DATE)
    find_and_click_image("appletarget/source_file_tab_down.png")
    find_and_click_image("appletarget/double_deceased.png")
    pyautogui.press("enter")


def end_time_recording(start_time):
    global FULL_DATE
    end_time = time.time()
    duration = end_time - start_time
    log_file = "apple_program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    global delay, MAX_ATTEMPTS, x_scale, y_scale, confidence
    box = None
    attempts = 0
    while box is None:
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(delay * 5)
        # print("Searching for image: " + image_filename)
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            os.system(
                f'osascript -e \'display notification "Could not find image {image_filename}" with title "Error"\''
            )
            break

    _, y, width, height = box
    image_cords_x = box.left / 2 + width / 4
    image_cords_y = box.top / 2 + height / 4

    return round(y / 2), (image_cords_x, image_cords_y)


def main():
    global initials, cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, EDUCATION, COM_NUM, delay
    input_str = pyautogui.prompt(
        text="Enter Initials, which computer number this is, and delay time -1 to quit",
        title="Enter Initials, which computer number this is, and delay time -1 to quit",
        default="DE, 1, 0.1",
    )
    initials, computer_number, delay = input_str.strip().split(",")
    screen_width, screen_height = pyautogui.size()
    x_scale = screen_width / 1440
    y_scale = screen_height / 900
    delay = float(delay.strip())
    COM_NUM = int(computer_number.strip())
    cutOffBottomY = screen_height
    cutOffTopY, CRM_cords = cutoff_section_of_screen("appletarget/blackbaud_CRM.png")
    cord_click(CRM_cords)

    while initials != "-1":
        start_time = time.time()

        get_to_dead_page()
        number_of_interactions = interactions_num_finder()
        interactions_section(number_of_interactions)
        deceased_form()
        move_to_communications()
        opt_out_form()

        end_time_recording(start_time)
        find_and_click_image(EDUCATION)  # TODO find a way to remove


if __name__ == "__main__":
    main()
