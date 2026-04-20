from playwright.sync_api import Page, expect

from automation_testing_playground.config.credentials import TestData


class LoginPage:
    """SauceDemo login — UI adaptation and assertions stay here (POM / façade)."""

    _USER = "#user-name"
    _PASSWORD = "#password"
    _LOGIN_BUTTON = "#login-button"
    _ERROR_BANNER = "h3[data-test='error']"
    _INVENTORY_LIST = ".inventory_list"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(TestData.BASE_URL)

    def login_with_valid_credentials(self) -> None:
        self.open()
        self.page.fill(self._USER, TestData.VALID_USER)
        self.page.fill(self._PASSWORD, TestData.VALID_PASSWORD)
        self.page.click(self._LOGIN_BUTTON)

    def submit_credentials(self, username: str | None, password: str | None) -> None:
        """Attempt login. Pass None to skip filling a field (e.g. empty username test)."""
        self.open()
        if username is not None:
            self.page.fill(self._USER, username)
        if password is not None:
            self.page.fill(self._PASSWORD, password)
        self.page.click(self._LOGIN_BUTTON)

    def assert_error_banner_visible(self) -> None:
        expect(self.page.locator(self._ERROR_BANNER)).to_be_visible()

    def assert_error_contains(self, text: str, timeout: int = 5000) -> None:
        expect(self.page.locator(self._ERROR_BANNER)).to_contain_text(text, timeout=timeout)

    def assert_inventory_visible(self) -> None:
        expect(self.page.locator(self._INVENTORY_LIST)).to_be_visible()
