# @Dimitry Ermakov
# @09/23/2023
import time
from datetime import datetime
import pyperclip
import keyboard
import pyautogui
import pytesseract
import os

from main_shared_functions import (
    extract_text_from_coordinates,
    cord_click,
    tab_command,
    extract_digits_from_text,
    detect_dates,
)

# Interactions: 2 = 79.14 bot; 75.66 no copy pasting, experienced, fast as possible human
# Interactions: 1 = 50.66 bot; 51.08 no copy pasting, experienced, fast as possible human

# TODO
# Protential improvements:
#   - Find a better way to know the number of interactions than using extract_text_from_coordinates
#   - Use mss to take screenshots instead of pyautogui
#   - Find workaround to recieves imprints and waits

# original_x_scale = 1440 / 2880
# original_y_scale = 900 / 1800

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
    # Initialize variables for locating the image
    box = None
    attempts = 0

    # Continue attempting to locate the image until found
    while box is None:
        # Attempt to locate the image on the screen within the specified region
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

        # Sleep to avoid excessive attempts
        time.sleep(delay * 5)

        # Increment the attempts count
        attempts += 1

        # Display an error notification if the maximum attempts are reached
        if attempts >= MAX_ATTEMPTS:
            os.system(
                f'osascript -e \'display notification "Could not find image {image_filename}" with title "Error" sound name "Glass"\''
            )

        # If the image is still not found and up_or_down is provided, simulate key presses
        if box is None and up_or_down is not None:
            pyautogui.press(up_or_down)
            pyautogui.press(up_or_down)
            pyautogui.press(up_or_down)
            time.sleep(delay * 5)

    x, y, width, height = box
    x = box.left / 2 + width / 4 + biasx
    y = box.top / 2 + height / 4 + biasy

    # Click on the found image if it's not in the specified list
    if image_filename not in [
        PRIMIS,
        EDUCATION,
        LOAD_OPT_OUT_WAIT,
        LOAD_OWNER_WAIT,
    ]:
        cord_click((x, y))


def get_to_dead_page():
    # Global variable used in this method
    global COM_NUM

    # Click on "constituents" and "updates" images
    find_and_click_image("appletarget/constituents.png")
    find_and_click_image("appletarget/updates.png")

    # Check the value of COM_NUM to determine further actions
    if COM_NUM == 2:
        find_and_click_image("appletarget/third_page.png")
    if COM_NUM == 3:
        find_and_click_image("appletarget/fifth_page.png")

    # Click on the "name" image with a vertical bias
    find_and_click_image("appletarget/name.png", 0, round(25 * y_scale))


def interactions_num_finder():
    # Global variables used in this method
    global delay

    while True:
        pretext = "Interactions: "
        try:
            # Extract text from a specific screen region
            text = extract_text_from_coordinates(
                round(420 * x_scale),
                round(1350 * y_scale),
                round(620 * x_scale),
                round(1400 * y_scale),
            )
            if pretext in text:
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
    # Click on the "status_alone" image and "edit_interaction" image
    find_and_click_image(
        "appletarget/status_alone.png",
        0,
        round(number_of_interactions * 30 * y_scale),
        "down",
    )
    find_and_click_image("appletarget/edit_interaction.png", 0, 0, "down")


def interactions_section(number_of_interactions):
    # Global variables used in this method
    global PRIMIS, LOAD_OWNER_WAIT

    # Click on the "interactions" image
    find_and_click_image("appletarget/interactions.png")

    # Click on the top interaction
    click_on_top_interaction(1)

    # Process the application for the first interaction
    process_application()

    if number_of_interactions > 1:
        for i in range(2, number_of_interactions):
            find_and_click_image(LOAD_OWNER_WAIT)
            click_on_top_interaction(i)
            # Process the application for subsequent interactions (not confirmed)
            process_application(False)

    # Click on PRIMIS, "personal_info," and "marked_deceased"
    find_and_click_image(PRIMIS, 0, 0, "up")
    find_and_click_image("appletarget/personal_info.png")
    find_and_click_image("appletarget/marked_deceased.png")


def process_application(is_confirmed=True):
    # Global variables used in this method
    global noted_date, initials, FULL_DATE, CRM_cords

    # Click on "tab_down_complete" image
    find_and_click_image("appletarget/tab_down_complete.png")

    if is_confirmed:
        # If confirmed, click on "completed_form" and "wait_for_complete" images
        find_and_click_image("appletarget/completed_form.png")
        find_and_click_image("appletarget/wait_for_complete.png")
    else:
        # If not confirmed, click on "declined" and "wait_for_decline" images
        find_and_click_image("appletarget/declined.png")
        find_and_click_image("appletarget/wait_for_decline.png")

    # Press tab 7 times
    tab_command(7)

    # Write FULL_DATE and copy it to clipboard
    keyboard.write(FULL_DATE)
    pyperclip.copy("")
    tab_command(3)
    keyboard.press("command+A")
    time.sleep(0.1)
    keyboard.press_and_release("command+C")
    found_text = pyperclip.paste()

    # Check if the found text indicates a date
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
        # Prompt for the noted date and click on "sites"
        noted_date = pyautogui.prompt(
            text="", title="Noted Date?", default=detect_dates(found_text)
        )
        find_and_click_image("appletarget/sites.png")

    # Press down, enter, and enter keys
    pyautogui.press("down")
    pyautogui.press("enter")
    pyautogui.press("enter")

    # Write a note based on confirmation status (Not Researched or Duplicate)
    if is_confirmed:
        keyboard.write("Note: Not Researched - " + initials)
    else:
        keyboard.write("Note: Duplicate - " + initials)

    tab_command(2)
    pyautogui.press("enter")


def deceased_form():
    # Global variables used in this method
    global noted_date, FORMATTED_DATE

    # Click on the "deceased_date" image
    find_and_click_image("appletarget/deceased_date.png")

    # Check if noted_date is "1/" and write the appropriate date
    if noted_date == "1/":
        keyboard.write(FORMATTED_DATE)
    elif noted_date != "1/":
        keyboard.write(noted_date)
        noted_date = "1/"

    # Click on "source_tab_down" and "communication_from," then press enter
    find_and_click_image("appletarget/source_tab_down.png")
    find_and_click_image("appletarget/communication_from.png")
    pyautogui.press("enter")


def move_to_communications():
    # Global variables used in this method
    global PRIMIS

    # Click on "constitute," PRIMIS, "communications," and "add" (simulating a down key press)
    find_and_click_image("appletarget/constitute.png")
    find_and_click_image(PRIMIS)
    find_and_click_image("appletarget/communications.png")
    find_and_click_image("appletarget/add.png", 0, 0, "down")


def opt_out_form():
    # Global variables used in this method
    global FULL_DATE

    # Click on "solicit_code" image and write "Imprimis"
    find_and_click_image("appletarget/solicit_code.png")
    keyboard.write("Imprimis")

    # Click on "imprimis_three" and "imprimis_done" images
    find_and_click_image("appletarget/imprimis_three.png")
    find_and_click_image("appletarget/imprimis_done.png")

    # Press tab key
    pyautogui.press("tab")

    # Press backspace 11 times to clear the text field
    for _ in range(0, 11):
        pyautogui.press("backspace")

    # Write "Opt-out"
    keyboard.write("Opt-out")

    # Click on "opt_out" image and press tab
    find_and_click_image("appletarget/opt_out.png")
    pyautogui.press("tab")

    # Write FULL_DATE and click on "source_file_tab_down" and "double_deceased," then press enter
    keyboard.write(FULL_DATE)
    find_and_click_image("appletarget/source_file_tab_down.png")
    find_and_click_image("appletarget/double_deceased.png")
    pyautogui.press("enter")


def end_time_recording(start_time):
    # Global variables used in this method
    global FULL_DATE

    # Calculate the duration and write it to a log file
    end_time = time.time()
    duration = end_time - start_time
    log_file = "time_logs/apple_program_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{duration:.2f}\n")


def cutoff_section_of_screen(image_filename):
    # Global variables used in this method
    global delay, MAX_ATTEMPTS, x_scale, y_scale, confidence

    box = None
    attempts = 0

    while box is None:
        # Locate the image on the screen with specified region and confidence level
        box = pyautogui.locateOnScreen(
            image_filename,
            confidence=confidence,
            region=(0, 0, round(2880 * x_scale), round(1800 * y_scale)),
        )
        time.sleep(delay * 5)
        attempts += 1

        # Display an error notification if image cannot be found after maximum attempts
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
    # Global variables used in this method
    global initials, cutOffTopY, x_scale, y_scale, CRM_cords, cutOffBottomY, EDUCATION, COM_NUM, delay

    # Prompt the user for input: initials, computer number, and delay time
    input_str = pyautogui.prompt(
        text="Enter Initials, which computer number this is, and delay time -1 to quit",
        title="Enter Initials, which computer number this is, and delay time -1 to quit",
        default="DE, 1, 0.01",
    )
    initials, computer_number, delay = input_str.strip().split(",")

    # Get the screen width and height
    screen_width, screen_height = pyautogui.size()

    # Calculate the x and y scale factors based on the screen size
    x_scale = screen_width / 1440
    y_scale = screen_height / 900

    # Parse the delay and computer number
    delay = float(delay.strip())
    COM_NUM = int(computer_number.strip())

    # Set cutOffBottomY to screen height
    cutOffBottomY = screen_height

    # Calculate cutOffTopY and CRM_cords using the cutoff_section_of_screen method
    cutOffTopY, CRM_cords = cutoff_section_of_screen("appletarget/blackbaud_CRM.png")

    # Click on CRM_cords
    cord_click(CRM_cords)

    # Main loop, continue until initials are "-1"
    while initials != "-1":
        start_time = time.time()

        # Navigate to the dead page
        get_to_dead_page()

        # Find the number of interactions
        number_of_interactions = interactions_num_finder()

        # Process interactions
        interactions_section(number_of_interactions)

        # Fill out the deceased form
        deceased_form()

        # Move to communications and fill out the opt-out form
        move_to_communications()
        opt_out_form()

        # Record end time and find_and_click_image for EDUCATION
        end_time_recording(start_time)
        find_and_click_image(EDUCATION)


if __name__ == "__main__":
    main()
