from playwright.sync_api import Page, expect
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage
from automation_testing_playground.config.credentials import TestData
from automation_testing_playground.helpers.log_helpers import InlineLogger

def test_valid_login(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Valid Login 🔐")

    login = LoginPage(page)
    logger.step("Attempting to login with valid credentials ✅")
    login.login_with_valid_credentials()

    expect(page.locator(".inventory_list")).to_be_visible()
    logger.success("🎉 Login successful! User landed on Inventory page 🛒")

    logger.summary(passed=1, failed=0, skipped=0)

def test_invalid_login(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Invalid Login Attempt 🚫")

    page.goto(TestData.BASE_URL)
    logger.note("Entering incorrect username and password ❌")
    page.fill("#user-name", TestData.INVALID_USER)
    page.fill("#password", TestData.INVALID_PASSWORD)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    logger.error("Expected error message displayed for invalid credentials ⚠️")

    logger.summary(passed=1, failed=0, skipped=0)

def test_login_empty_username(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Login Attempt with Empty Username 🚫")

    page.goto(TestData.BASE_URL)
    logger.note("Leaving username empty and entering valid password 🗒️")
    page.fill("#password", TestData.VALID_PASSWORD)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    logger.error("Error message correctly displayed for missing username ❗")

    logger.summary(passed=1, failed=0, skipped=0)

def test_login_empty_password(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Login Attempt with Empty Password 🚫")

    page.goto(TestData.BASE_URL)
    logger.note("Entering valid username and leaving password empty 🗒️")
    page.fill("#user-name", TestData.VALID_USER)
    page.click("#login-button")

    expect(page.locator("h3[data-test='error']")).to_be_visible()
    logger.error("Error message correctly displayed for missing password ❗")

    logger.summary(passed=1, failed=0, skipped=0)
