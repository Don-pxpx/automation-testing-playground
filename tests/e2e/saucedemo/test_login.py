from playwright.sync_api import Page

from automation_testing_playground.config.credentials import TestData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage


def test_valid_login(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Valid Login 🔐")

    login = LoginPage(page)
    logger.step("Attempting to login with valid credentials ✅")
    login.login_with_valid_credentials()

    login.assert_inventory_visible()
    logger.success("🎉 Login successful! User landed on Inventory page 🛒")

    logger.summary(passed=1, failed=0, skipped=0)


def test_invalid_login(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Invalid Login Attempt 🚫")

    login = LoginPage(page)
    logger.note("Entering incorrect username and password ❌")
    login.submit_credentials(TestData.INVALID_USER, TestData.INVALID_PASSWORD)

    login.assert_error_banner_visible()
    logger.error("Expected error message displayed for invalid credentials ⚠️")

    logger.summary(passed=1, failed=0, skipped=0)


def test_login_empty_username(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Login Attempt with Empty Username 🚫")

    login = LoginPage(page)
    logger.note("Leaving username empty and entering valid password 🗒️")
    login.submit_credentials(None, TestData.VALID_PASSWORD)

    login.assert_error_banner_visible()
    logger.error("Error message correctly displayed for missing username ❗")

    logger.summary(passed=1, failed=0, skipped=0)


def test_login_empty_password(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Login Attempt with Empty Password 🚫")

    login = LoginPage(page)
    logger.note("Entering valid username and leaving password empty 🗒️")
    login.submit_credentials(TestData.VALID_USER, None)

    login.assert_error_banner_visible()
    logger.error("Error message correctly displayed for missing password ❗")

    logger.summary(passed=1, failed=0, skipped=0)
