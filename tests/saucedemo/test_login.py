from seleniumbase import BaseCase
from pages.saucedemo_pages.login_page import LoginPage
from config.credentials import TestData
from helpers.log_helpers import InlineLogger  # 👈 Import InlineLogger

class SauceDemoLoginTests(BaseCase):

    def test_valid_login(self):
        logger = InlineLogger()
        logger.step("Starting Test: Valid Login 🔐")

        login = LoginPage(self)
        logger.step("Attempting to login with valid credentials ✅")
        login.login_with_valid_credentials()

        self.assert_element(".inventory_list")
        logger.success("🎉 Login successful! User landed on Inventory page 🛒")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_invalid_login(self):
        logger = InlineLogger()
        logger.step("Starting Test: Invalid Login Attempt 🚫")

        self.open(TestData.BASE_URL)
        logger.note("Entering incorrect username and password ❌")
        self.type("#user-name", "wrong_user")
        self.type("#password", "wrong_pass")
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        logger.error("Expected error message displayed for invalid credentials ⚠️")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_login_empty_username(self):
        logger = InlineLogger()
        logger.step("Starting Test: Login Attempt with Empty Username 🚫")

        self.open(TestData.BASE_URL)
        logger.note("Leaving username empty and entering valid password 🗒️")
        self.type("#password", TestData.VALID_PASSWORD)
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        logger.error("Error message correctly displayed for missing username ❗")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_login_empty_password(self):
        logger = InlineLogger()
        logger.step("Starting Test: Login Attempt with Empty Password 🚫")

        self.open(TestData.BASE_URL)
        logger.note("Entering valid username and leaving password empty 🗒️")
        self.type("#user-name", TestData.VALID_USER)
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        logger.error("Error message correctly displayed for missing password ❗")

        logger.summary(passed=1, failed=0, skipped=0)
