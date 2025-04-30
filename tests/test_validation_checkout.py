import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

@pytest.mark.validation
def test_checkout_form_submit_success(driver):
    wait = WebDriverWait(driver, 10)

    # Login
    driver.get("https://bookcart.azurewebsites.net/")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']"))).click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))).send_keys("testuserqa")
    driver.find_element(By.XPATH, "//input[@formcontrolname='password']").send_keys("StrongPassword1", Keys.ENTER)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))
    time.sleep(0.5)

    # Add to cart and go to checkout
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Add to Cart')]]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[contains(text(),'shopping_cart')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='CheckOut']"))).click()

    wait.until(EC.url_contains("/checkout"))
    time.sleep(0.5)

    # Fill form
    form_data = {
        "name": "John Doe",
        "addressLine1": "123 Main St",
        "addressLine2": "Apartment 456",
        "pincode": "710000",
        "state": "Tuzla"
    }

    for field, value in form_data.items():
        input_el = wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@formcontrolname='{field}']")))
        input_el.clear()
        input_el.send_keys(value)
        time.sleep(0.2)

    # Submit form
    place_order_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Place Order']")))
    driver.execute_script("arguments[0].click();", place_order_btn)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/myorders"))
    assert "/myorders" in driver.current_url
    print("✅ Checkout form submitted and redirected to /myorders.")
