class LoginPage:
    def __init__(self, base):
        self.base = base  # This will be `self` from BaseCase in the test class

    def login_with_valid_credentials(self):
        self.base.open("https://www.saucedemo.com/")
        self.base.type("#user-name", "standard_user")
        self.base.type("#password", "secret_sauce")
        self.base.click("#login-button")
