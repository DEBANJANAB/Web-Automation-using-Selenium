import json
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_configuration(config_file):
    with open(config_file, "r") as file:
        return json.load(file)

def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--headless")

    driver_path = r"C:\Users\parit\Downloads\edgedriver_win64 (1)\msedgedriver.exe"  # Adjust the path
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    
    return driver

def perform_action(driver, action, wait_time):
    wait = WebDriverWait(driver, wait_time)

    if action["action"] == "click":
        locator_type = action["locator"]["type"]
        locator_value = action["locator"]["value"]
        
        if locator_type == "LINK_TEXT":
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, locator_value)))
        elif locator_type == "ID":
            element = wait.until(EC.element_to_be_clickable((By.ID, locator_value)))
        # Add more locator types as needed
        
        element.click()
        print(f"Clicked on element with {locator_type} = {locator_value}")

    elif action["action"] == "back":
        driver.back()
        print("Went back to the previous page.")
        time.sleep(wait_time)

    elif action["action"] == "scroll_and_click":
        locator_type = action["locator"]["type"]
        locator_value = action["locator"]["value"]
        
        if locator_type == "LINK_TEXT":
            element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, locator_value)))
        # Add more locator types as needed

        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(wait_time)  # Optional sleep before clicking
        element.click()
        print(f"Scrolled to and clicked on element with {locator_type} = {locator_value}")

def main(config_file):
    # Step 1: Load configuration
    config = load_configuration(config_file)
    
    # Step 2: Set up WebDriver
    driver = setup_driver()
    
    try:
        # Step 3: Open the web application
        driver.get(config["url"])
        driver.maximize_window()
        print(f"Website {config['url']} opened successfully!")
        
        # Step 4: Perform actions based on config
        for action in config["actions"]:
            perform_action(driver, action, action.get("wait_time", 10))
        
    finally:
        # Step 5: Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)
