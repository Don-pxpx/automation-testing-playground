import pytest
from playwright.sync_api import Page

from automation_testing_playground.config.credentials import TestData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username,password,expected_substring,req_id",
    [
        (None, TestData.VALID_PASSWORD, "Username is required", "SDC-LOGIN-003"),
        (TestData.VALID_USER, None, "Password is required", "SDC-LOGIN-004"),
        (TestData.INVALID_USER, TestData.VALID_PASSWORD, "locked out", "SDC-LOGIN-005"),
        (
            TestData.VALID_USER,
            TestData.INVALID_PASSWORD,
            "Username and password do not match",
            "SDC-LOGIN-006",
        ),
    ],
    ids=[
        "SDC-LOGIN-003-empty-username",
        "SDC-LOGIN-004-empty-password",
        "SDC-LOGIN-005-locked-out",
        "SDC-LOGIN-006-wrong-password",
    ],
)
def test_login_negative_scenarios(
    page: Page,
    username: str | None,
    password: str | None,
    expected_substring: str,
    req_id: str,
):
    """Parameterized login negatives (SDC-LOGIN-003–006); req_id passed per case."""
    logger = InlineLogger()
    logger.step(f"Starting negative login scenario ({req_id})")

    login = LoginPage(page)
    login.submit_credentials(username, password)

    login.assert_error_banner_visible()
    login.assert_error_contains(expected_substring, timeout=5000)
    logger.error(f"Expected error displayed for {req_id}")

    logger.summary(passed=1, failed=0, skipped=0)
