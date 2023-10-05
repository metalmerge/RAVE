# RAVE - Repetitive Automation Via Efficiency

RAVE is a Python script designed to automate repetitive tasks on a website by simulating keyboard and mouse actions. This script is specifically tailored to streamline the process of editing data objects in Blackbaud CRM. Please use this script responsibly and ensure that you comply with the terms of use and ethical considerations of the website you are interacting with.

## Requirements

Before using RAVE, make sure you have the following prerequisites installed:

1. **Python 3.x**: Download and install Python 3.x. Make sure it's added to your PATH and not installed with administrative privileges. You can download Python from [Python.org](https://www.python.org/downloads/).

2. **Tesseract OCR**: RAVE uses Tesseract OCR for text recognition. If you are having trouble with Tesseract, you can download it directly at the [Tesseract GitHub Wiki](https://github.com/UB-Mannheim/tesseract/wiki).

3. **Python Libraries**: Install the necessary Python libraries by running the following commands in your terminal or command prompt:

   ```bash
   pip install pyperclip keyboard pyautogui pytesseract opencv-python-headless
   ```

## Usage

1. Clone or download the RAVE repository to your local machine.

2. Navigate to the RAVE directory:

3. Run one of these two commands depending on your computer:

   ```bash
   python3 apple_main.py
   ```

   ```bash
   python windows_main.py
   ```

## Troubleshooting

- If you encounter a 'TypeError: `<' not supported between instances of 'str' and 'int''` error when running pyautogui, you can find a solution [here](https://stackoverflow.com/questions/76361049/how-to-fix-typeerror-not-supported-between-instances-of-str-and-int-wh/76383784#76383784).

## Acknowledgments

Special thanks to Coding 101 with Steve and Indently for their informative videos on Pyautogui:

- [Coding 101 with Steve](https://www.youtube.com/watch?v=qIJpBz6R2Uw)
- [Indently](https://www.youtube.com/watch?v=cZQDO0ktnrw)
