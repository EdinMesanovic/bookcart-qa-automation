import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


@pytest.mark.ui
def test_category_filter_and_price_slider(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://bookcart.azurewebsites.net/")
    time.sleep(2)

    expected_categories = ["All Categories", "Biography", "Fiction", "Mystery", "Fantasy", "Romance"]

    for category_name in expected_categories:
        category_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//mat-list-item//span[contains(text(), '{category_name}')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", category_element)
        time.sleep(0.5)
        category_element.click()
        time.sleep(1)
        print(f"✅ Clicked category: {category_name}")

    price_slider = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-slider")
    ))
    driver.execute_script("arguments[0].scrollIntoView(true);", price_slider)
    time.sleep(1)

    slider_thumb = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".mdc-slider__thumb-knob")
    ))

    actions = ActionChains(driver)
    actions.click_and_hold(slider_thumb).move_by_offset(-170, 0).release().perform()
    time.sleep(2)

    print("✅ Price slider moved successfully!")


@pytest.mark.ui
def test_ui_pages_success(driver):
    wait = WebDriverWait(driver, 10)
    base_url = "https://bookcart.azurewebsites.net"

    # 1. no login needed urls
    public_pages = [
        {"url": "/", "element": (By.XPATH, "//span[contains(text(),'Login')]")},
        {"url": "/login", "element": (By.XPATH, "//button//span[normalize-space()='Login']")},
        {"url": "/register", "element": (By.XPATH, "//button//span[normalize-space()='Register']")},
    ]

    for page in public_pages:
        driver.get(base_url + page["url"])
        try:
            wait.until(EC.presence_of_element_located(page["element"]))
            print(f"✅ Stranica {page['url']} učitana uspješno.")
        except:
            pytest.fail(f"❌ Stranica {page['url']} nije uspješno učitana ili element nije pronađen.")

    # 2. login
    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(),'Login')]")))
    login_button.click()

    username_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@formcontrolname='username']")))
    password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")

    username_input.send_keys("testuserqa")  
    password_input.send_keys("StrongPassword1")
    password_input.send_keys(Keys.ENTER)

    wait.until(EC.url_to_be("https://bookcart.azurewebsites.net/"))

    # 3. test content
    protected_pages = [
        {"url": "/shopping-cart", "element": (By.XPATH, "//mat-card-title[contains(text(),'Shopping cart')]")},
        {"url": "/checkout", "element": (By.XPATH, "//span[normalize-space()='Place Order']")},
    ]

    for page in protected_pages:
        driver.get(base_url + page["url"])
        try:
            wait.until(EC.presence_of_element_located(page["element"]))
            print(f"✅ Stranica {page['url']} učitana uspješno (nakon login-a).")
        except:
            pytest.fail(f"❌ Stranica {page['url']} nije uspješno učitana ili element nije pronađen.")

