from playwright.sync_api import Page, expect
from automation_testing_playground.config.credentials import TestData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage

def test_locked_out_user_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Locked-out user cannot login 🚫")

    page.goto(TestData.BASE_URL)
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", TestData.VALID_PASSWORD)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    expect(page.locator("h3[data-test='error']")).to_contain_text("locked out", timeout=5000)
    logger.error("Locked-out message displayed as expected")

    logger.summary(passed=1, failed=0, skipped=0)

def test_empty_username_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Empty username shows error ❗")

    page.goto(TestData.BASE_URL)
    page.fill("#password", TestData.VALID_PASSWORD)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    expect(page.locator("h3[data-test='error']")).to_contain_text("Username is required", timeout=5000)
    logger.error("Username required error displayed")

    logger.summary(passed=1, failed=0, skipped=0)

def test_empty_password_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Empty password shows error ❗")

    page.goto(TestData.BASE_URL)
    page.fill("#user-name", TestData.VALID_USER)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    expect(page.locator("h3[data-test='error']")).to_contain_text("Password is required", timeout=5000)
    logger.error("Password required error displayed")

    logger.summary(passed=1, failed=0, skipped=0)

def test_wrong_credentials_show_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Wrong credentials show error 🔐❌")

    page.goto(TestData.BASE_URL)
    page.fill("#user-name", TestData.VALID_USER)
    page.fill("#password", TestData.INVALID_PASSWORD)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    expect(page.locator("h3[data-test='error']")).to_contain_text("Username and password do not match", timeout=5000)
    logger.error("Mismatch credentials error displayed")

    logger.summary(passed=1, failed=0, skipped=0)
