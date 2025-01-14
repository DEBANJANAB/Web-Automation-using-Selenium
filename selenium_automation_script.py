from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Step 1: Set up WebDriver

options = Options()
options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
options.add_argument("--disable-web-security")      # Optional: Disable web security
options.add_argument("--allow-running-insecure-content")  # Allow insecure content
options.add_argument("--headless")

driver_path = r"C:\Users\parit\Downloads\edgedriver_win64 (1)\msedgedriver.exe"  
service = Service(driver_path)
driver = webdriver.Edge(service=service)

try:
    # Step 2: Open the web application
    driver.get("https://practice-automation.com/")  
   
    driver.maximize_window()
    print("Website opened successfully!")

    wait = WebDriverWait(driver, 10) 

    # Step 3: Perform actions
    # Example: Locate a button and click
   
    button = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "JavaScript Delays"))  # Use visible text
    )

    # Step 3: Click the button
    button.click()
    print("Clicked 'JavaScript Delays' button.")

    time.sleep(3)

    #Go back to the home page
    driver.back()

    time.sleep(2)    
    
    # Step 6: Scroll down to another button
    next_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Click Events"))  # Adjust the locator
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    time.sleep(2) 

    # Step 7: Click the next button
    next_button.click()
    print("Clicked the second button!")


finally:
    # Step 5: Close the browser
    driver.quit()
    print("Browser closed.")
