import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import os

def load_config(config_file):
    """Load configuration from a JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)

def setup_driver(driver_path, browser_type="edge"):
    """Setup the WebDriver for different browsers and return the driver instance."""
    if browser_type.lower() == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized") 
        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    elif browser_type.lower() == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--start-maximized") 
        driver = webdriver.Firefox(service=FirefoxService(driver_path), options=firefox_options)
    elif browser_type.lower() == "edge":
        driver = webdriver.Edge(service=EdgeService(driver_path))
    else:
        print(f"Browser '{browser_type}' not supported.")
        sys.exit(1)
    
    return driver

def login(driver, url, username_input, password_input):
    """Perform login action"""
    driver.get(url)
    
    try:
        # Wait for the username field to be available
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'user-name'))
        )
        password = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'login-button')

        username.send_keys(username_input)
        password.send_keys(password_input)
        login_button.click()
        print("Login attempted with provided credentials.")
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        sys.exit(1)

def verify_login(driver):
    """Verify successful login on Sauce Demo."""
    try:
       
        inventory_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'title'))
        )
        print(f"Login successful. Page title: {inventory_title.text}")
        assert "Products" in inventory_title.text
    except Exception as e:
        print(f"Login failed or unexpected error: {e}")
        print("Current page source:\n", driver.page_source)
        driver.quit()
        sys.exit(1)

def inspect_elements(driver, tag_name=None, attribute=None):
    """Inspect elements on the Sauce Demo page and print the desired attributes."""
    try:
        elements = driver.find_elements(By.TAG_NAME, tag_name) if tag_name else driver.find_elements(By.XPATH, "//*")
        print(f"Found {len(elements)} elements matching the criteria.")

        for element in elements[:10]:  # Limit to first 10 elements to avoid overwhelming output
            attr_value = element.get_attribute(attribute) if attribute else element.text
            print(f"Element: {element.tag_name}, {attribute or 'text'}: {attr_value}")

    except Exception as e:
        print(f"Error inspecting elements: {e}")

def main():
    """Main function to execute the script."""
    if len(sys.argv) != 2:
        print("Usage: script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    
   
    config = load_config(config_file)

    url = config['url']
    username_input = config['username']
    password_input = config['password']
    driver_path = config['driver_path']
    browser_type = config.get('browser', 'chrome').lower()  
    tag_name = config.get('tag_name', None)  
    attribute = config.get('attribute', None)

   
    if not os.path.exists(driver_path):
        print(f"Driver path '{driver_path}' not found!")
        sys.exit(1)

    driver = setup_driver(driver_path, browser_type)
    
    login(driver, url, username_input, password_input)
    verify_login(driver)

    if tag_name or attribute:
        print("\nInspecting elements on the page:")
        inspect_elements(driver, tag_name, attribute)

    
    driver.quit()

if __name__ == "__main__":
    main()
