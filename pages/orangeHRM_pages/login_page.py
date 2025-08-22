from helpers.log_helpers import InlineLogger

class LoginPage:
    def __init__(self, test):
        self.test = test
        self.logger = InlineLogger()
        # Locators
        self.username_field = "input[name='username']"
        self.password_field = "input[name='password']"
        self.login_button = "button[type='submit']"
        # Updated: include the full class combo for the Dashboard header
        self.dashboard_marker = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"

    def open_login(self):
        self.logger.step("Open OrangeHRM Login Page")
        self.test.open("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.test.assert_element(self.username_field)

    def login(self, username, password):
        self.logger.step("Enter login credentials")
        self.test.type(self.username_field, username)
        self.test.type(self.password_field, password)
        self.test.click(self.login_button)

    def is_logged_in(self):
        self.logger.step("Check if dashboard is visible")
        return self.test.is_element_visible(self.dashboard_marker)

