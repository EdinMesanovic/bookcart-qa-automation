# Bookcart QA Automation

## 📋 Requirements

- Python 3.8+
- Google Chrome browser
- ChromeDriver

## Project Overview
Testing the demo e-commerce application:  
🔗 [https://bookcart.azurewebsites.net/](https://bookcart.azurewebsites.net/)

The goal is to validate the core user flows (smoke tests) and ensure that the main functionalities are working properly.

---

### Scope of Testing
- User Registration
- User Login / Logout
- Adding items to the shopping cart
- Clearing the cart
- Product Search
- Checkout process
- Basic UI loading verification (important pages)

---

### Tools Used
- **Selenium WebDriver** for browser automation
- **Pytest** as the test framework
- **Python 3.13**
- Browser: **Chrome**

---

### Test Strategy
- **Smoke Tests**: Focused on critical user journeys.
- **Positive Test Cases**: Normal flow with valid inputs.
- **Negative Test Cases**: Invalid inputs, missing fields.
- **UI Verification**: Check that important pages load correctly.

---

### Notes
- Small time delays (`time.sleep()`) were added to make the test execution smoother and more visually traceable.
- Random usernames are generated dynamically during registration to avoid duplication.

---

## 📦 Installation and Setup

1. Clone the repository:
    ```
    git clone https://github.com/EdinMesanovic/bookcart-qa-automation.git
    cd bookcart-qa-automation
    ```

2. Create and activate a virtual environment:
   ```bash
   /bookcart-qa-automation> python -m venv venv
   /bookcart-qa-automation> source venv/bin/activate  # For Linux/Mac
   /bookcart-qa-automation> venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the tests:
   ```bash
    python run.py
   ```
