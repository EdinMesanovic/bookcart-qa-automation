import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.mark.validation
def test_checkout_form_submit_success(driver):
    wait = WebDriverWait(driver, 10)
    
    # 1. Login
    driver.get("https://bookcart.azurewebsites.net/")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']")))
    login_button.click()

    username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']")))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
    username_input.send_keys("mesantest")
    password_input.send_keys("StrongPassword1")
    password_input.send_keys(Keys.ENTER)
    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))
    time.sleep(1)

    add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Add to Cart')]]")))
    driver.execute_script("arguments[0].click();", add_to_cart)
    time.sleep(1)

    cart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[contains(text(),'shopping_cart')]")))
    driver.execute_script("arguments[0].click();", cart_icon)
    time.sleep(1)

    
    checkout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='CheckOut']")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    wait.until(EC.url_contains("/checkout"))
    time.sleep(1)

    
    fields = {
        "name": "John Doe",
        "addressLine1": "123 Main St",
        "addressLine2": "Apartment 456",
        "pincode": "710000",
        "state": "Tuzla"
    }

    for name, value in fields.items():
        input_field = wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@formcontrolname='{name}']")))
        input_field.clear()
        input_field.send_keys(value)
        time.sleep(0.3)

    place_order_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Place Order']")))
    driver.execute_script("arguments[0].click();", place_order_btn)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/myorders"))

    assert "/myorders" in driver.current_url
    print("✅ Checkout form submitted and redirected to /myorders.")
