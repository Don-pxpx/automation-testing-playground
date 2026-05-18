import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from automation_testing_playground.config.orangeHRM_credentials import OrangeHRMData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.orangehrm_models import LoginCredentials
from automation_testing_playground.pages.orangeHRM_pages.login_page import LoginPage

fake = Faker()


@pytest.mark.smoke
def test_login_valid_and_invalid(page: Page):
    """OHR-AUTH-001: Valid login reaches dashboard; invalid login shows error (correctness)."""
    logger = InlineLogger()
    login = LoginPage(page)

    logger.step("Login with VALID credentials")
    login.open_login()
    logger.note(f"Navigating to {OrangeHRMData.BASE_URL}")

    credentials = LoginCredentials(
        username=OrangeHRMData.USERNAME,
        password=OrangeHRMData.PASSWORD,
    )
    login.login_with_credentials(credentials)

    expect(page.locator(login.dashboard_marker)).to_be_visible()
    assert login.is_logged_in()
    logger.success("VALID login landed on dashboard")

    logger.step("Login with INVALID credentials")
    login.start_fresh_login_session()

    bad_user = fake.user_name()
    bad_pass = fake.password()
    logger.note(f"Trying invalid credentials → user: {bad_user}")

    login.submit_login_attempt(bad_user, bad_pass)
    error_text = login.assert_login_error_contains(
        "Invalid credentials",
        "CSRF token validation failed",
    )
    logger.success(f"INVALID login correctly shows error: {error_text}")
