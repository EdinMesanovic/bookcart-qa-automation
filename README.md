# 📦 Bookcart QA Automation

## 📋 Requirements

- Python 3.8+
- Google Chrome browser
- ChromeDriver

---

## 🔍 Project Overview

Testing the demo e-commerce application:  
🔗 [https://bookcart.azurewebsites.net/](https://bookcart.azurewebsites.net/)

The goal is to validate the **core user flows** (smoke tests) and ensure that the main functionalities are working properly.

---

## ✅ Scope of Testing

- User Registration
- User Login / Logout
- Adding items to the shopping cart
- Clearing the cart
- Product Search
- Checkout process (positive and negative)
- UI and category filtering
- Page load verification (basic UI)

---

## 🧪 Tools Used

- **Selenium WebDriver** – browser automation
- **Pytest** – test framework
- **Python 3.13**
- **Chrome browser**

---

## 🧠 Test Strategy

- **Smoke Tests**: Cover the main user flows like login, cart, and checkout.
- **Positive Test Cases**: Normal flow with valid inputs.
- **Negative Test Cases**: Invalid login, form validation, mismatched passwords.
- **UI Verification**: Ensure important pages and filters load correctly.

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

## 🛠️ Custom CLI Tool

A command-line interface is available for selecting which type of tests to run:
   ```bash
    python run.py
   ```

## 🔍 Additional Notes on Implementation

> While the assignment required only automation of smoke tests, this project intentionally goes beyond:

- ✅ **Full test coverage** including smoke, positive, negative, validation, and UI
- ✅ **Reusable helper functions** to avoid repetition
- ✅ **Time delays added** to improve stability and visual clarity
- ✅ **Dynamic data generation** to avoid conflicts (e.g. random usernames)
- ✅ **Bug reports written** with proper structure and reasoning

This approach reflects critical thinking and simulates real-world QA automation practices in professional environments.

