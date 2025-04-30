import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Helpers
def navigate_to_login(driver, wait):
    driver.get("https://bookcart.azurewebsites.net/")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']")))
    login_button.click()

def navigate_to_register(driver, wait):
    navigate_to_login(driver, wait)
    signup_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Register']")))
    signup_link.click()

def fill_input_fields(driver, field_data):
    for field, value in field_data:
        field.click()
        field.clear()
        field.send_keys(value)
        driver.execute_script("arguments[0].blur();", field)
        time.sleep(0.2)

@pytest.mark.negative
def test_login_invalid_credentials(driver):
    wait = WebDriverWait(driver, 10)
    navigate_to_login(driver, wait)

    username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']")))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")

    username_input.send_keys("wronguser")
    password_input.send_keys("wrongpassword", Keys.ENTER)

    time.sleep(1)
    assert "/login" in driver.current_url
    print("✅ Login with invalid credentials test passed successfully.")

@pytest.mark.negative
def test_signup_mismatched_passwords(driver):
    wait = WebDriverWait(driver, 10)
    navigate_to_register(driver, wait)

    # form
    first_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='firstName']")))
    last_name = driver.find_element(By.XPATH, "//input[@formcontrolname='lastName']")
    username_input = driver.find_element(By.XPATH, "//input[@formcontrolname='userName']")
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    confirm_password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']")
    gender_male = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Male')]")))

    random_username = f"invaliduser{int(time.time())}"
    fields = [
        (first_name, "Invalid"),
        (last_name, "User"),
        (username_input, random_username),
        (password_input, "Password123"),
        (confirm_password_input, "Password321"),
    ]
    fill_input_fields(driver, fields)
    gender_male.click()

    register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Register']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
    driver.execute_script("arguments[0].click();", register_button)

    time.sleep(2)
    assert "/register" in driver.current_url
    print("✅ Signup with mismatched passwords test passed successfully.")

@pytest.mark.negative
def test_checkout_form_validation(driver):
    wait = WebDriverWait(driver, 10)

    # Login
    navigate_to_login(driver, wait)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))).send_keys("mesantest")
    driver.find_element(By.XPATH, "//input[@formcontrolname='password']").send_keys("StrongPassword1", Keys.ENTER)
    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))

    # Add to cart i checkout
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Add to Cart')]]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[contains(text(),'shopping_cart')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='CheckOut']"))).click()
    wait.until(EC.url_contains("/checkout"))

    time.sleep(1)
    # click blur
    for name in ["name", "addressLine1", "addressLine2", "pincode", "state"]:
        field = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@formcontrolname='{name}']")))
        field.click()
        driver.execute_script("arguments[0].blur();", field)
        time.sleep(0.2)

    place_order = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Place Order']")))
    driver.execute_script("arguments[0].click();", place_order)

    for error_text in ["Name is required", "Address is required", "Pincode is required", "State is required"]:
        assert wait.until(EC.presence_of_element_located((By.XPATH, f"//mat-error[contains(text(), '{error_text}')]"))).is_displayed()

    print("✅ Negativni test za validaciju checkout forme uspješno prošao.")
