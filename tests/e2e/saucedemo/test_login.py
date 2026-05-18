import pytest
from playwright.sync_api import Page

from automation_testing_playground.config.credentials import TestData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login(page: Page):
    """SDC-LOGIN-001: Valid credentials open the inventory page (functional correctness)."""
    logger = InlineLogger()
    logger.step("Starting Test: Valid Login 🔐")

    login = LoginPage(page)
    logger.step("Attempting to login with valid credentials ✅")
    login.login_with_valid_credentials()

    login.assert_inventory_visible()
    logger.success("🎉 Login successful! User landed on Inventory page 🛒")

    logger.summary(passed=1, failed=0, skipped=0)


def test_invalid_login(page: Page):
    """SDC-LOGIN-002: Invalid credentials show an error banner (functional correctness)."""
    logger = InlineLogger()
    logger.step("Starting Test: Invalid Login Attempt 🚫")

    login = LoginPage(page)
    logger.note("Entering incorrect username and password ❌")
    login.submit_credentials(TestData.INVALID_USER, TestData.INVALID_PASSWORD)

    login.assert_error_banner_visible()
    logger.error("Expected error message displayed for invalid credentials ⚠️")

    logger.summary(passed=1, failed=0, skipped=0)
