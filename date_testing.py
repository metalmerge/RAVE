import re
from datetime import datetime


def extract_date(input_text):
    months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    day_month_year_result = day_month_year_only(input_text)
    if day_month_year_result is not None:
        return day_month_year_result
    month_year_result = month_year_only(input_text, months)
    if month_year_result is not None:
        return month_year_result
    year_only_result = year_only(input_text)
    if year_only_result is not None:
        return year_only_result

    # Regular expression pattern to match different date formats.
    date_pattern = r"\b(\d{1,2})[ /-](\d{4})\b|\b([A-Za-z]+)[ /-](\d{4})\b"
    matches = re.findall(date_pattern, input_text)

    if matches:
        for match in matches:
            if match[0]:  # Matched day and year (e.g., 10/2023 or 10-2023)
                month, year = match[0], match[1]
                return f"{month}/{year}"
            elif match[2] in months:  # Check if the matched text is a valid month name
                month, year = months[match[2]], match[3]
                return f"{month}/{year}"

    # Handle the case of "month YYYY"
    month_year_pattern = r"\b([A-Za-z]+) (\d{4})\b"
    month_year_match = re.search(month_year_pattern, input_text)
    if month_year_match:
        month, year = months[month_year_match.group(1)], month_year_match.group(2)
        return f"{month:02d}/{year}"

    # Handle special cases for phrases like "last month," "last year," and "this year."
    return special_cases(input_text)


def day_month_year_only(input_text):
    date_pattern = r"\b(\d{1,2})[ /-](\d{1,2})[ /-](\d{4})\b"
    matches = re.findall(date_pattern, input_text)
    if matches:
        for match in matches:
            month, year = match[0], match[2]
            if month.startswith("0"):
                month = month[1]  # Remove leading zero
            return f"{month}/{year}"
    return None


def year_only(input_text):
    year_pattern = r"\b(\d{4})\b"
    year_match = re.search(year_pattern, input_text)
    if year_match:
        year = year_match.group(1)
        return f"1/{year}"
    return None


def month_year_only(input_text, months):
    month_year_pattern = r"\b([A-Za-z]+)[ /-](\d{4})\b"
    month_year_match = re.search(month_year_pattern, input_text)
    if month_year_match:
        month = months.get(month_year_match.group(1))
        year = month_year_match.group(2)
        if month:
            return f"{month}/{year}"
    return None


def special_cases(input_text):
    CURRENT_DATE = datetime.now()
    formatted_month = str(CURRENT_DATE.month)
    formatted_year = str(CURRENT_DATE.year)
    if "last month" in input_text:
        last_month = int(formatted_month) - 1
        return f"{last_month}/{formatted_year}"

    if "last year" in input_text:
        last_year = int(formatted_year) - 1
        return f"1/{last_year}"

    if "this year" in input_text:
        return f"1/{formatted_year}"
    if "this month" in input_text:
        return f"{formatted_month}/{formatted_year}"

    return "1/"


def test_date_detection():
    # Define test cases with input text and expected output dates
    test_cases = [
        {
            "input_text": "June 2017",
            "expected_date": "6/2017",
        },
        {
            "input_text": "10-15-2023",
            "expected_date": "10/2023",
        },
        {
            "input_text": "9/15/2023",
            "expected_date": "9/2023",
        },
        {
            "input_text": "2023",
            "expected_date": "1/2023",
        },
        {
            "input_text": "last month",
            "expected_date": f"{datetime.now().month - 1}/{datetime.now().year}",
        },
        {
            "input_text": "How was 2017",
            "expected_date": "1/2017",
        },
        {
            "input_text": "last year",
            "expected_date": f"1/{datetime.now().year - 1}",
        },
        {
            "input_text": "this year",
            "expected_date": f"1/{datetime.now().year}",
        },
        {
            "input_text": "August 2022",
            "expected_date": "8/2022",
        },
        {
            "input_text": "20 December 2023.",
            "expected_date": "12/2023",
        },
        {
            "input_text": "this month",
            "expected_date": f"{datetime.now().month}/{datetime.now().year}",
        },
        {
            "input_text": "2023",
            "expected_date": "1/2023",
        },
        {
            "input_text": "April 2021",
            "expected_date": "4/2021",
        },
    ]

    # Run tests and print results
    for i, test_case in enumerate(test_cases):
        result = extract_date(test_case["input_text"])
        expected = test_case["expected_date"]
        if result == expected:
            print(f"Test {i + 1}: PASSED")
        else:
            print(f"Test {i + 1}: FAILED")
            print(f"  Input Text: {test_case['input_text']}")
            print(f"  Expected Date: {expected}")
            print(f"  Detected Date: {result}")
        print()


# Run the tests
test_date_detection()
