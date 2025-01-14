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
   # driver.get("https://debanjanab.github.io/")
    driver.maximize_window()
    print("Website opened successfully!")

    wait = WebDriverWait(driver, 10) 

    # Step 3: Perform actions
    # Example: Locate a button and click
   # button = driver.find_element(By.XPATH, "//a[contains(text(), 'Products')]")
   # button = driver.find_element(By.CSS_SELECTOR, ".wp-block-button__link wp-element-button")
    #button.click()
    button = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "JavaScript Delays"))  # Use visible text
    )

    # Step 3: Click the button
    button.click()
    print("Clicked 'JavaScript Delays' button.")

    # Example: Locate a search bar and perform a search
    search_bar = driver.find_element(By.CSS_SELECTOR, ".card-footer-item")  
    search_bar.send_keys("Electric bikes" + Keys.RETURN)
    print("Performed a search for 'Electric bikes'.")

    # Step 4: Pause for demonstration purposes
   

finally:
    # Step 5: Close the browser
    driver.quit()
    print("Browser closed.")
