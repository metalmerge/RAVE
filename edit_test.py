import pyautogui
from PIL import Image
import time

# Load the image from your file path
image = Image.open("/Users/dimaermakov/Downloads/google.png")

# Use a while loop to ensure the image is found

res = pyautogui.locateCenterOnScreen(image, confidence=0.9)
print(res)

# Move to the found coordinates and click
pyautogui.moveTo(322, 24, duration=0.25)
pyautogui.click()

# Type the text
pyautogui.typewrite("Sample Input")

# Add a delay to ensure the actions are performed
time.sleep(3)
