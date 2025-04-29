import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Global
created_username = ""
created_password = "Test1234"

def login(driver, username, password):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(0.5)

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='mdc-button__label' and normalize-space()='Login']")))
    login_button.click()
    time.sleep(0.5)

    username_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@formcontrolname='username']")))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))
    time.sleep(0.5)

@pytest.mark.smoke
def test_signup_success(driver):
    global created_username

    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(0.5)

    # Login > Register
    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Login']")))
    login_button.click()
    time.sleep(0.5)

    signup_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Register']")))
    signup_link.click()
    time.sleep(0.5)

    # Form
    first_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='firstName']")))
    last_name = driver.find_element(By.XPATH, "//input[@formcontrolname='lastName']")
    username_input = driver.find_element(By.XPATH, "//input[@formcontrolname='userName']")
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    confirm_password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']")
    gender_male = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Male')]")))

    random_number = str(int(time.time()))
    random_username = f"testuser{random_number}"
    created_username = random_username

    fields = [
        (first_name, "Test"),
        (last_name, "User"),
        (username_input, random_username),
        (password_input, created_password),
        (confirm_password_input, created_password),
    ]

    for field, value in fields:
        field.click()
        field.clear()
        field.send_keys(value)
        driver.execute_script("arguments[0].blur();", field)
        time.sleep(0.3)

    gender_male.click()
    time.sleep(0.3)

    register_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='Register']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
    driver.execute_script("arguments[0].click();", register_button)

    time.sleep(2)

    wait.until(EC.url_contains("/login"))
    assert "/login" in driver.current_url
    time.sleep(1)

@pytest.mark.smoke
def test_login_success(driver):
    login(driver, 'mesantest', 'StrongPassword1')

    wait = WebDriverWait(driver, 10)

    user_profile_link = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(., 'mesantest')]")))
    time.sleep(0.5)

    assert "mesantest" in user_profile_link.text

@pytest.mark.smoke
def test_logout_success(driver):
    login(driver, 'mesantest', 'StrongPassword1')

    wait = WebDriverWait(driver, 10)

    user_menu = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(., 'mesantest')]")))
    user_menu.click()
    time.sleep(0.5)

    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button//span[normalize-space()='Logout']")))
    logout_button.click()

    wait.until(EC.url_contains("/login"))
    assert "/login" in driver.current_url
    time.sleep(1)

@pytest.mark.smoke
def test_add_and_clear_cart_success(driver):
    wait = WebDriverWait(driver, 10)

    login(driver, 'mesantest', 'StrongPassword1')

    add_to_cart_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[contains(text(),'Add to Cart')]]")))
    driver.execute_script("arguments[0].click();", add_to_cart_button)
    time.sleep(1)

    cart_icon = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//mat-icon[contains(text(),'shopping_cart')]")))
    driver.execute_script("arguments[0].click();", cart_icon)
    time.sleep(1)

    clear_cart_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Clear cart']")))
    driver.execute_script("arguments[0].click();", clear_cart_button)

    continue_shopping_button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[normalize-space()='Continue shopping']")))
    time.sleep(0.5)

    assert continue_shopping_button.is_displayed()
    print("✅ Add to cart + Clear cart test passed successfully!")

@pytest.mark.smoke
def test_search(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(0.5)

    search_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Search books or authors']")
    ))
    search_input.click()
    search_input.clear()
    search_input.send_keys("Slayer")
    time.sleep(0.5)

    suggestion = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//mat-option//span[contains(text(), 'Slayer')]")
    ))
    suggestion.click()

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[@href='/books/details/21']")
    ))
    time.sleep(1)

    assert driver.find_element(By.XPATH, "//a[@href='/books/details/21']").is_displayed()
    time.sleep(1)

@pytest.mark.smoke
def test_checkout_success(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(0.5)

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='mdc-button__label' and normalize-space()='Login']")))
    login_button.click()
    time.sleep(0.5)

    username_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@formcontrolname='username']")))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    username_input.send_keys('mesantest')
    password_input.send_keys('StrongPassword1')
    password_input.send_keys(Keys.ENTER)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))
    time.sleep(0.5)

    add_to_cart_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[contains(text(),'Add to Cart')]]")))
    driver.execute_script("arguments[0].click();", add_to_cart_button)
    time.sleep(0.5)

    cart_icon = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//mat-icon[contains(text(),'shopping_cart')]")))
    driver.execute_script("arguments[0].click();", cart_icon)
    time.sleep(0.5)

    checkout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='CheckOut']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
    driver.execute_script("arguments[0].click();", checkout_button)

    wait.until(EC.url_contains("/checkout"))
    time.sleep(1)

    assert "/checkout" in driver.current_url
