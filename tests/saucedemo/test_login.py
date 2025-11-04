from playwright.sync_api import Page, expect
from pages.saucedemo_pages.login_page import LoginPage
from config.credentials import TestData

class TestSauceDemoLogin:

    def test_valid_login(self, page: Page):
        print("🟡 Starting: test_valid_login")
        login = LoginPage(page)
        login.login_with_valid_credentials()
        expect(page.locator(".inventory_list")).to_be_visible()
        print("✅ Login successful! 🎉")

    def test_invalid_login(self, page: Page):
        print("🟡 Starting: test_invalid_login")
        page.goto(TestData.BASE_URL)
        page.fill("#user-name", "wrong_user")
        page.fill("#password", "wrong_pass")
        page.click("#login-button")
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        print("❌ Login failed as expected! 🔐")

    def test_login_empty_username(self, page: Page):
        print("🚫 Starting: test_login_empty_username")
        page.goto(TestData.BASE_URL)
        page.fill("#password", TestData.VALID_PASSWORD)
        page.click("#login-button")
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        print("❗ Error message displayed for missing username")

    def test_login_empty_password(self, page: Page):
        print("🚫 Starting: test_login_empty_password")
        page.goto(TestData.BASE_URL)
        page.fill("#user-name", TestData.VALID_USER)
        page.click("#login-button")
        expect(page.locator("h3[data-test='error']")).to_be_visible()
        print("❗ Error message displayed for missing password")
