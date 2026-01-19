from playwright.sync_api import Page, expect
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.orangehrm_models import LoginCredentials

class LoginPage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object
        self.logger = InlineLogger()
        # Locators
        self.username_field = "input[name='username']"
        self.password_field = "input[name='password']"
        self.login_button = "button[type='submit']"
        # Updated: include the full class combo for the Dashboard header
        self.dashboard_marker = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"

    def open_login(self):
        """Open OrangeHRM login page."""
        self.logger.step("Open OrangeHRM Login Page")
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        # Wait for Vue.js to render the login form
        self.page.wait_for_selector(self.username_field, timeout=15000)

    def login(self, username: str, password: str):
        """Login with username and password."""
        self.logger.step("Enter login credentials")
        self.page.fill(self.username_field, username)
        self.page.fill(self.password_field, password)
        self.page.click(self.login_button)
        # Wait for login to complete and dashboard to load
        self.page.wait_for_selector(self.dashboard_marker, timeout=10000)

    def login_with_credentials(self, credentials: LoginCredentials):
        """Login using Pydantic model."""
        self.login(credentials.username, credentials.password)

    def is_logged_in(self) -> bool:
        """Check if dashboard is visible (user is logged in)."""
        self.logger.step("Check if dashboard is visible")
        return self.page.locator(self.dashboard_marker).is_visible()

