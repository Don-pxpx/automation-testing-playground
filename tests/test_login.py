from seleniumbase import BaseCase
from pages.login_page import LoginPage
from config.credentials import TestData

class SauceDemoLoginTests(BaseCase):

    def test_valid_login(self):
        print("🟡 Starting: test_valid_login")
        login = LoginPage(self)
        login.login_with_valid_credentials()
        self.assert_element(".inventory_list")
        print("✅ Login successful! 🎉")

    def test_invalid_login(self):
        print("🟡 Starting: test_invalid_login")
        self.open(TestData.BASE_URL)
        self.type("#user-name", "wrong_user")
        self.type("#password", "wrong_pass")
        self.click("#login-button")
        self.assert_element("h3[data-test='error']")
        print("❌ Login failed as expected! 🔐")

    def test_login_empty_username(self):
        print("🚫 Starting: test_login_empty_username")
        self.open(TestData.BASE_URL)
        self.type("#password", TestData.VALID_PASSWORD)
        self.click("#login-button")
        self.assert_element("h3[data-test='error']")
        print("❗ Error message displayed for missing username")

    def test_login_empty_password(self):
        print("🚫 Starting: test_login_empty_password")
        self.open(TestData.BASE_URL)
        self.type("#user-name", TestData.VALID_USER)
        self.click("#login-button")
        self.assert_element("h3[data-test='error']")
        print("❗ Error message displayed for missing password")
