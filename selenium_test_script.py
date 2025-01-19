from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time


url=input("Enter the url: ")
username_input=input("Enter the username: ")
password_input=input("Enter the password: ")
 
driver_path = r"C:\Users\parit\Downloads\edgedriver_win64 (1)\msedgedriver.exe"  
service = Service(driver_path)
driver = webdriver.Edge(service=service)
    

driver.get(url)

# Find the username and password input fields and login button
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

# Perform login action
username.send_keys(username_input)  # Replace with valid username for testing
password.send_keys(password_input)  # Replace with valid password
login_button.click()

# Wait for the page to load after login (optional but sometimes necessary)
time.sleep(2)  # You can also use WebDriverWait for better control

# Verify login success
try:
    # Check if the "Welcome" message or some specific element is present after login
    welcome_message = driver.find_element(By.XPATH, '//*[contains(text(), "Welcome")]')  # Searching for text "Welcome"
    print(welcome_message.text)  # Print the text to verify what was returned
    assert "Welcome to the Secure Area" in welcome_message.text
except AssertionError:
    print("Login failed or message not found.")
    print("Current page source:\n", driver.page_source)  # Print the page source to inspect

# Close the browser
driver.quit()
