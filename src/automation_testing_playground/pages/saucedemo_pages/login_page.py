class LoginPage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def login_with_valid_credentials(self):
        self.page.goto("https://www.saucedemo.com/")
        self.page.fill("#user-name", "standard_user")
        self.page.fill("#password", "secret_sauce")
        self.page.click("#login-button")
