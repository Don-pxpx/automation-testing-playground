from playwright.sync_api import Page

from automation_testing_playground.config.credentials import TestData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage


def test_locked_out_user_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Locked-out user cannot login 🚫")

    login = LoginPage(page)
    login.submit_credentials(TestData.INVALID_USER, TestData.VALID_PASSWORD)

    login.assert_error_banner_visible()
    login.assert_error_contains("locked out", timeout=5000)
    logger.error("Locked-out message displayed as expected")

    logger.summary(passed=1, failed=0, skipped=0)


def test_empty_username_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Empty username shows error ❗")

    login = LoginPage(page)
    login.submit_credentials(None, TestData.VALID_PASSWORD)

    login.assert_error_banner_visible()
    login.assert_error_contains("Username is required", timeout=5000)
    logger.error("Username required error displayed")

    logger.summary(passed=1, failed=0, skipped=0)


def test_empty_password_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Empty password shows error ❗")

    login = LoginPage(page)
    login.submit_credentials(TestData.VALID_USER, None)

    login.assert_error_banner_visible()
    login.assert_error_contains("Password is required", timeout=5000)
    logger.error("Password required error displayed")

    logger.summary(passed=1, failed=0, skipped=0)


def test_wrong_credentials_show_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Wrong credentials show error 🔐❌")

    login = LoginPage(page)
    login.submit_credentials(TestData.VALID_USER, TestData.INVALID_PASSWORD)

    login.assert_error_banner_visible()
    login.assert_error_contains("Username and password do not match", timeout=5000)
    logger.error("Mismatch credentials error displayed")

    logger.summary(passed=1, failed=0, skipped=0)
