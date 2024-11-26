
# Aviator Round History Scraper

A Python script to automate login, extract round history from the Aviator game on Betika, and store the data in a SQLite database.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [How to Use](#how-to-use)
- [Notes](#notes)
- [License](#license)

## Features
- Automates login to Betika (requires manual navigation to the Aviator game after login).
- Extracts payout data and stores it in a SQLite database.
- Alerts the user if no new data is detected for 3 minutes.

## Requirements
- **Python 3.x**
- The following Python libraries:
  - `selenium`
  - `playsound`
  - `sqlite3` (comes with Python by default)
- **Google Chrome** browser.
- **ChromeDriver**: Must be installed and compatible with your version of Chrome.

## Setup and Installation
1. Install Python and ensure it’s added to your PATH.
2. Install required libraries:
   ```bash
   pip install selenium playsound
Download ChromeDriver:
Match the version to your Chrome browser.
Add the chromedriver file to your system PATH or provide its path in the script:
python

driver = webdriver.Chrome(executable_path="path/to/chromedriver")
Update the script with your Betika login details:
python

phone_input.send_keys("your phone number")  # Replace with your phone number
password_input.send_keys("your password")  # Replace with your password
How to Use
Run the script:
bash

python aviator_scraper.py
Log in automatically using your credentials.
Manually navigate to the Aviator game after logging in.
Let the script extract payout data and save it in the SQLite database (aviator_rounds35_1.db).
If no data is detected for 3 minutes, the script will play an alert sound.
Notes
Ensure that ChromeDriver is correctly installed and matches your Chrome version.
The SQLite database (aviator_rounds35_1.db) will be created in the same directory as the script.
The alert sound file path (extractionfail.wav) may need to be updated.
License
This project is licensed under the MIT License. Feel free to use and modify it.

