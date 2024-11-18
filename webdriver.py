from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the path to the WebDriver
driver_path = "C:/chromedrive/chromedriver-win64/chromedriver.exe"  # Ensure this points to the correct executable

# Initialize the Service
service = Service(driver_path)

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--headless")  # Uncomment if you want headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Betika login page
driver.get("https://www.betika.com/")

# Wait for the page to load
time.sleep(5)  # Initial wait


# Login function
def login(phone_number, password):
    try:
        print("Waiting for phone number input...")
        # Wait for the phone number input field to be present and then enter the phone number
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='e.g. 0712 234567']"))
        )
        print("Phone number input found.")
        phone_input.send_keys(phone_number)

        print("Waiting for password input...")
        # Wait for the password input field to be present and then enter the password
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        print("Password input found.")
        password_input.send_keys(password)

        print("Waiting for login button...")
        # Wait for the login button to be present and click it
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'session__form__button') and span[text()='Login']]"))
        )
        print("Login button found. Clicking...")
        login_button.click()

        time.sleep(5)  # Wait for login to complete
        print("Login attempt completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Close the browser after finishing


# Call login function
phone_number = "0741962080"  # Replace with your Betika phone number
password = "kipruto030"  # Replace with your Betika password
login(phone_number, password)
