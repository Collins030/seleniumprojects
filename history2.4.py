import sqlite3
import time
from datetime import datetime
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the database connection
conn = sqlite3.connect('aviator_rounds35_1.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS round_history (
                    timestamp TEXT, 
                    payout REAL
                 )''')
conn.commit()

# Selenium setup
driver = webdriver.Chrome()  # Ensure ChromeDriver is in PATH or provide its path here
driver.get("https://www.betika.com/en-ke/login")

# Track last stored payout to avoid duplicates
last_payouts = set()  # Store unique payouts in a set
last_extraction_time = time.time()  # Store the last time data was successfully extracted


# Login logic with enhanced error handling
def login():
    try:
        # Check if already logged in
        if "aviator" in driver.current_url:
            print("Already logged in and on the Aviator page.")
            return True

        # Locate and fill in the phone number
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'].input"))
        )
        phone_input.send_keys("your phone number")  # Replace with actual phone number

        # Locate and fill in the password
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'].input"))
        )
        password_input.send_keys("you password")  # Replace with actual password

        # Locate and click the login button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".account__payments__submit.session__form__button.login"))
        )
        ActionChains(driver).move_to_element(login_button).click(login_button).perform()
        print("Login button clicked!")

        # Wait to ensure redirection to the aviator page
        WebDriverWait(driver, 20).until(EC.url_contains("aviator"))
        return True

    except Exception as e:
        print("Error during login:", e)
        return False


# Attempt to login and navigate to the Aviator page
if login():
    driver.get("https://www.betika.com/en-ke/aviator")
else:
    driver.quit()
    exit()

# Switch to the Aviator iframe
try:
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "aviator-iframe")))
    print("Switched to Aviator iframe successfully.")
except Exception as e:
    print("Error switching to Aviator iframe:", e)
    driver.quit()
    exit()


# Function to extract and store round history with duplicate checks and delays
def extract_and_store_round_history():
    global last_payouts, last_extraction_time

    try:
        # Locate the main result-history container
        result_history_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.result-history.disabled-on-game-focused.my-2"))
        )

        # Find all bubble-multiplier elements within this container
        payouts = result_history_container.find_elements(By.CLASS_NAME, "bubble-multiplier")

        # Only capture unique payouts
        new_data_extracted = False  # Flag to check if any new data is extracted
        for payout in payouts:
            multiplier_text = payout.text.strip()  # Clean up the text
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Check if the payout is new
            if multiplier_text and multiplier_text not in last_payouts:
                last_payouts.add(multiplier_text)  # Add to the set to avoid duplicates

                # Insert new data into the database
                cursor.execute("INSERT INTO round_history (timestamp, payout) VALUES (?, ?)",
                               (timestamp, multiplier_text))
                conn.commit()
                print("New round history entry stored:", timestamp, multiplier_text)
                new_data_extracted = True  # Mark that new data has been extracted

        if new_data_extracted:
            last_extraction_time = time.time()  # Update the last extraction time if new data is found

            # Check if it's been more than 2 minutes (120 seconds) since the last extraction
            if time.time() - last_extraction_time > 120:
                print("No new data detected in the last 2 minutes. Refreshing page...")
                driver.refresh()
                last_extraction_time = time.time()  # Reset the timer after refreshing

        # Check if it's been more than 3 minutes (180 seconds) since the last extraction
        if time.time() - last_extraction_time > 180:
            print("No new data detected in the last 3 minutes. Triggering alarm...")
            playsound("C:/Users/User/Documents/Audacity/extractionfail.wav")  # Play alert sound
            last_extraction_time = time.time()  # Reset the timer after alerting

        # Delay to wait for new data
        time.sleep(5)

        # Reset last_payouts if it gets too large (avoid memory issues)
        if len(last_payouts) > 100:
            last_payouts.clear()

    except Exception as e:
        print("Error extracting round history:", e)


# Loop to continuously check for new round data
try:
    while True:
        extract_and_store_round_history()

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    # Close the database and driver
    conn.close()
    driver.quit()
