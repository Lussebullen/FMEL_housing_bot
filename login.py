from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from os import getenv
from dotenv import load_dotenv
import time
import datetime

def fmel_navigate():
    options = Options()
    # Leave window open when done if True
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager()
                                            .install()), options=options)

    # Login url doesn't seem static, so use generic base url, then navigate
    fmel_url = "https://accommodation.fmel.ch/StarRezPortal"

    driver.get(fmel_url)
    driver.maximize_window()

    # Find all links, click the login link
    links = driver.find_elements("xpath", "//a[@href]")
    for link in links:
        if "<strong>Login</strong>" in link.get_attribute('innerHTML'):
            link.click()
            break

    # Locate login form
    field_username = driver.find_element(By.NAME, "Username")
    field_password = driver.find_element(By.NAME, "Password")

    # Fill login form
    load_dotenv()
    field_username.send_keys(getenv("FMEL_USERNAME"))
    field_password.send_keys(getenv("FMEL_PASSWORD"))

    # Click login button
    login_button = driver.find_element(By.CSS_SELECTOR,"button[aria-label=Login]")
    login_button.click()

    time.sleep(3)

    # Click "Book a room" > "Apply"
    driver.find_element(By.LINK_TEXT,"Book a room").click()
    driver.find_element(By.CSS_SELECTOR,"button[aria-label=Apply]").click()

    time.sleep(3)

    # Parse potential dates
    start_dates = {}

    dates = driver.find_elements(By.XPATH,"//span[@class='ui-notification-content multiline markdown']/ul/li")
    for date in dates:
        date_string = date.get_attribute('innerHTML').strip()
        day_of_week = datetime.datetime.strptime(date_string, '%d %b %Y').strftime('%a')
        start_date = day_of_week + ", " + date_string
        start_dates[start_date] = False

    LACKING_RESULTS = "Currently not available"
    available_dates = []

    for date, flag in start_dates.items():
        time.sleep(5)
        # select start date form
        field = driver.find_element(By.NAME,"DateStart")
        # change value to desired date -- javascript execution
        driver.execute_script("arguments[0].setAttribute('value',arguments[1]);",field,date)
        time.sleep(1)
        button = driver.find_element(By.CSS_SELECTOR,"button[aria-label=Continue]")
        button.send_keys(Keys.RETURN)

        time.sleep(10) # Let results load
        results = driver.find_element(By.CLASS_NAME,"ui-results")
        
        body = results.get_attribute('innerHTML')

        # Add available housing to list
        if LACKING_RESULTS not in body:
            available_dates.append(date)
    
        back_button = driver.find_element(By.CSS_SELECTOR,"button[aria-label='Go Back']")
        back_button.send_keys(Keys.RETURN)
        confirm_button = driver.find_element(By.CSS_SELECTOR,"button[aria-label='Yes']")
        confirm_button.send_keys(Keys.RETURN)
        
    return available_dates