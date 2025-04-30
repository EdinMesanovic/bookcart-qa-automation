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

@pytest.mark.negative
def test_checkout_form_validation(driver):
    wait = WebDriverWait(driver, 10)

    #  Login
    driver.get("https://bookcart.azurewebsites.net/")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']"))).click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))).send_keys("mesantest")
    driver.find_element(By.XPATH, "//input[@formcontrolname='password']").send_keys("StrongPassword1", Keys.ENTER)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))

    #  Add to cart and go to checkout
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Add to Cart')]]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[contains(text(),'shopping_cart')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='CheckOut']"))).click()

    wait.until(EC.url_contains("/checkout"))
    time.sleep(1)

    field_names = ["name", "addressLine1", "addressLine2", "pincode", "state"]
    for field_name in field_names:
        input_field = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@formcontrolname='{field_name}']")))
        input_field.click()
        driver.execute_script("arguments[0].blur();", input_field)
        time.sleep(0.2)

    place_order_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Place Order']")))
    driver.execute_script("arguments[0].click();", place_order_btn)

    error_texts = [
        "Name is required",
        "Address is required",
        "Pincode is required",
        "State is required"
    ]
    for error in error_texts:
        assert wait.until(EC.presence_of_element_located((By.XPATH, f"//mat-error[contains(text(), '{error}')]"))).is_displayed()

    print("✅ Negativni test za validaciju checkout forme uspješno prošao.")