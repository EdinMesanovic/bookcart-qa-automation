import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

@pytest.mark.validation
def test_register_empty_fields_validation(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")

    # Register form
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']")))
    login_btn.click()

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Register']")))
    register_link.click()

    # Click register
    register_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Register']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", register_btn)
    driver.execute_script("arguments[0].click();", register_btn)

    # click and blur for validation
    form_fields = [
        "//input[@formcontrolname='firstName']",
        "//input[@formcontrolname='lastName']",
        "//input[@formcontrolname='userName']",
        "//input[@formcontrolname='password']",
        "//input[@formcontrolname='confirmPassword']"
    ]

    for xpath in form_fields:
        field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.click()
        driver.execute_script("arguments[0].blur();", field)
        time.sleep(0.2) 

    time.sleep(2) 
    
    error_messages = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//mat-error")
    ))
    time.sleep(2) 
    assert len(error_messages) >= 1

@pytest.mark.validation
def test_login_empty_fields_validation(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")

    # Go login
    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='mdc-button__label' and normalize-space()='Login']")
    ))
    login_button.click()

    # click login
    login_submit_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='Login']]")
    ))
    driver.execute_script("arguments[0].click();", login_submit_button)

    # click and blur for validation
    form_fields = [
        "//input[@formcontrolname='username']",
        "//input[@formcontrolname='password']"
    ]

    for xpath in form_fields:
        field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.click()
        driver.execute_script("arguments[0].blur();", field)
        time.sleep(0.5)

    time.sleep(2)
    
    error_messages = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//mat-error")
    ))
    time.sleep(0.5)
    assert len(error_messages) >= 1

@pytest.mark.validation
def test_login_invalid_credentials(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")

    # go Login
    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='mdc-button__label' and normalize-space()='Login']")
    ))
    login_button.click()

    username_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@formcontrolname='username']")
    ))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")

    username_input.send_keys("wronguser")
    password_input.send_keys("wrongpassword")
    password_input.send_keys(Keys.ENTER)

    # Wait
    time.sleep(2)

    assert "/login" in driver.current_url
