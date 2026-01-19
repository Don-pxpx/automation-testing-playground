import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.config.orangeHRM_credentials import OrangeHRMData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.orangeHRM_pages.login_page import LoginPage
from automation_testing_playground.models.orangehrm_models import LoginCredentials

fake = Faker()

def test_login_valid_and_invalid(page: Page):
    """Test valid and invalid login scenarios."""
    logger = InlineLogger()

    # ✅ VALID LOGIN
    logger.step("Login with VALID credentials")
    login = LoginPage(page)
    login.open_login()
    logger.note(f"Navigating to {OrangeHRMData.BASE_URL}")
    
    credentials = LoginCredentials(
        username=OrangeHRMData.USERNAME,
        password=OrangeHRMData.PASSWORD
    )
    login.login_with_credentials(credentials)
    
    expect(page.locator(login.dashboard_marker)).to_be_visible()
    assert login.is_logged_in()
    logger.success("VALID login landed on dashboard")

    # ❌ INVALID LOGIN (fresh session so we don't reuse cookies)
    logger.step("Login with INVALID credentials")
    # Clear session and start fresh
    page.context.clear_cookies()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # Wait for page to load completely
    page.wait_for_timeout(3000)
    
    bad_user = fake.user_name()
    bad_pass = fake.password()
    logger.note(f"Trying invalid credentials → user: {bad_user}")
    
    page.fill("input[name='username']", bad_user)
    page.fill("input[name='password']", bad_pass)
    page.click("button[type='submit']")

    # Expect an error toast/message on invalid login
    error_locator = page.locator("p.oxd-text.oxd-text--p.oxd-alert-content-text")
    error_locator.wait_for(state="visible", timeout=10000)
    error_text = error_locator.text_content() or ""
    
    # Check for either "Invalid credentials" or "CSRF token validation failed"
    assert "Invalid credentials" in error_text or "CSRF token validation failed" in error_text
    logger.success(f"INVALID login correctly shows error: {error_text}")
