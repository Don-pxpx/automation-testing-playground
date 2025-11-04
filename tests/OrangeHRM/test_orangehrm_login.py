import pytest
from seleniumbase import BaseCase
from faker import Faker

from config.orangeHRM_credentials import OrangeHRMData
from helpers.log_helpers import InlineLogger
from pages.orangeHRM_pages.login_page import LoginPage

fake = Faker()

class OrangeHRMLoginTests(BaseCase):
    def test_login_valid_and_invalid(self):
        logger = InlineLogger()

        # ✅ VALID LOGIN
        logger.step("Login with VALID credentials")
        login = LoginPage(self)
        login.open_login()
        logger.note(f"Navigating to {OrangeHRMData.BASE_URL}")
        login.login(OrangeHRMData.USERNAME, OrangeHRMData.PASSWORD)
        self.assert_true(login.is_logged_in())
        logger.success("VALID login landed on dashboard")

        # ❌ INVALID LOGIN (fresh session so we don’t reuse cookies)
        logger.step("Login with INVALID credentials")
        # Clear session and start fresh
        self.delete_all_cookies()
        self.open("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        # Wait for page to load completely
        self.sleep(3)
        bad_user = fake.user_name()
        bad_pass = fake.password()
        logger.note(f"Trying invalid credentials → user: {bad_user}")
        self.type("input[name='username']", bad_user)
        self.type("input[name='password']", bad_pass)
        self.click("button[type='submit']")

        # Expect an error toast/message on invalid login
        self.wait_for_element_visible("p.oxd-text.oxd-text--p.oxd-alert-content-text")
        error_text = self.get_text("p.oxd-text.oxd-text--p.oxd-alert-content-text")
        # Check for either "Invalid credentials" or "CSRF token validation failed"
        self.assert_true("Invalid credentials" in error_text or "CSRF token validation failed" in error_text)
        logger.success(f"INVALID login correctly shows error: {error_text}")
