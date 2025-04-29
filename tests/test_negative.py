import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

@pytest.mark.negative
def test_login_invalid_credentials(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Login']")))
    login_button.click()

    username_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@formcontrolname='username']")))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")

    username_input.send_keys("wronguser")
    password_input.send_keys("wrongpassword")
    password_input.send_keys(Keys.ENTER)

    time.sleep(1)

    assert "/login" in driver.current_url
    print("✅ Login with invalid credentials test passed successfully.")

@pytest.mark.negative
def test_signup_mismatched_passwords(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Login']")))
    login_button.click()

    signup_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Register']")))
    signup_link.click()

    first_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@formcontrolname='firstName']")))
    last_name = driver.find_element(By.XPATH, "//input[@formcontrolname='lastName']")
    username_input = driver.find_element(By.XPATH, "//input[@formcontrolname='userName']")
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    confirm_password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']")
    gender_male = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(., 'Male')]")))

    random_number = str(int(time.time()))
    random_username = f"invaliduser{random_number}"

    fields = [
        (first_name, "Invalid"),
        (last_name, "User"),
        (username_input, random_username),
        (password_input, "Password123"),
        (confirm_password_input, "Password321"),  # mismatched passwords
    ]

    for field, value in fields:
        field.click()
        field.clear()
        field.send_keys(value)
        driver.execute_script("arguments[0].blur();", field)
        time.sleep(0.2)

    gender_male.click()

    register_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='Register']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
    driver.execute_script("arguments[0].click();", register_button)

    time.sleep(2)
    assert "/register" in driver.current_url
    print("✅ Signup with mismatched passwords test passed successfully.")