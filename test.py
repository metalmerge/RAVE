from date_extractor import extract_dates
from windows_main import formatted_extract_date

# crate a bunch of test cases for the date extractor
test_cases = [
    "Email indicated she passed away 8 years ago",
    "12/12/20",
    "12/12/2020",
    "Please mark constituent as deceased -- 2018 - By user: bredding",
]

# loop through the test cases and print the results
for test_case in test_cases:
    print(extract_dates(test_case))
    print(formatted_extract_date(test_case))
# [datetime.datetime(1937, 1, 4, 0, 0, tzinfo=<UTC>)]
