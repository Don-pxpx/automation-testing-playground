from seleniumbase import BaseCase

from config.credentials import TestData
from helpers.log_helpers import InlineLogger
from pages.saucedemo_pages.login_page import LoginPage


class SauceDemoLoginEdgeCases(BaseCase):

    def test_locked_out_user_shows_error(self):
        logger = InlineLogger()
        logger.step("Starting Test: Locked-out user cannot login 🚫")

        self.open(TestData.BASE_URL)
        self.type("#user-name", "locked_out_user")
        self.type("#password", TestData.VALID_PASSWORD)
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        self.assert_text("locked out", "h3[data-test='error']", timeout=5)
        logger.error("Locked-out message displayed as expected")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_empty_username_shows_error(self):
        logger = InlineLogger()
        logger.step("Starting Test: Empty username shows error ❗")

        self.open(TestData.BASE_URL)
        self.type("#password", TestData.VALID_PASSWORD)
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        self.assert_text("Username is required", "h3[data-test='error']", timeout=5)
        logger.error("Username required error displayed")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_empty_password_shows_error(self):
        logger = InlineLogger()
        logger.step("Starting Test: Empty password shows error ❗")

        self.open(TestData.BASE_URL)
        self.type("#user-name", TestData.VALID_USER)
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        self.assert_text("Password is required", "h3[data-test='error']", timeout=5)
        logger.error("Password required error displayed")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_wrong_credentials_show_error(self):
        logger = InlineLogger()
        logger.step("Starting Test: Wrong credentials show error 🔐❌")

        self.open(TestData.BASE_URL)
        self.type("#user-name", TestData.VALID_USER)
        self.type("#password", TestData.INVALID_PASSWORD)
        self.click("#login-button")

        self.assert_element("h3[data-test='error']")
        self.assert_text("Username and password do not match", "h3[data-test='error']", timeout=5)
        logger.error("Mismatch credentials error displayed")

        logger.summary(passed=1, failed=0, skipped=0)


