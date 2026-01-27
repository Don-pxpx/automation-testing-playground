from automation_testing_playground.config.credentials import TestData


class LoginPage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def login_with_valid_credentials(self):
        self.page.goto(TestData.BASE_URL)
        self.page.fill("#user-name", TestData.VALID_USER)
        self.page.fill("#password", TestData.VALID_PASSWORD)
        self.page.click("#login-button")
