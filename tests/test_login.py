from seleniumbase import BaseCase
from config.credentials import TestData

class SauceDemoLoginTests(BaseCase):

    def test_valid_login(self):
        print("🟡 Starting: test_valid_login")

        self.open(TestData.BASE_URL)
        print("🔗 Navigated to SauceDemo")

        self.type("#user-name", TestData.VALID_USER)
        print("👤 Entered valid username")

        self.type("#password", TestData.VALID_PASSWORD)
        print("🔒 Entered valid password")

        self.click("#login-button")
        print("👉 Clicked login")

        self.assert_text("Products", "span.title")
        print("✅ Login successful! 🎉")

    def test_invalid_login(self):
        print("🟡 Starting: test_invalid_login")

        self.open(TestData.BASE_URL)
        print("🔗 Navigated to SauceDemo")

        self.type("#user-name", TestData.INVALID_USER)
        print("👤 Entered invalid username")

        self.type("#password", TestData.INVALID_PASSWORD)
        print("🔒 Entered invalid password")

        self.click("#login-button")
        print("👉 Clicked login")

        self.assert_element("h3[data-test='error']")
        print("❌ Login failed as expected! 🔐")
