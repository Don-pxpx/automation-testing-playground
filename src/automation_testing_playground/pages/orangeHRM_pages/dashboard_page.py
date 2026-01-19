from playwright.sync_api import Page
from automation_testing_playground.helpers.log_helpers import InlineLogger

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object
        self.logger = InlineLogger()
        # Locators
        self.dashboard_marker = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"
        # Menu locators - using text content since href might be dynamic
        self.pim_menu = "ul.oxd-main-menu li:nth-child(2) a"
        self.admin_menu = "ul.oxd-main-menu li:nth-child(1) a"
        self.leave_menu = "ul.oxd-main-menu li:nth-child(3) a"
        self.time_menu = "ul.oxd-main-menu li:nth-child(4) a"
        self.recruitment_menu = "ul.oxd-main-menu li:nth-child(5) a"
        self.my_info_menu = "ul.oxd-main-menu li:nth-child(6) a"
        self.performance_menu = "ul.oxd-main-menu li:nth-child(7) a"
        self.dashboard_menu = "ul.oxd-main-menu li:nth-child(8) a"

    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is visible after login"""
        self.logger.step("Verify dashboard is loaded")
        return self.page.locator(self.dashboard_marker).is_visible()

    def goto_pim(self):
        """Navigate to PIM (Personal Information Management) section"""
        self.logger.step("Navigate to PIM section")
        self.page.wait_for_selector(self.pim_menu, timeout=10000)
        self.page.click(self.pim_menu)
        # Wait for PIM page to load
        self.page.wait_for_selector("h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module", timeout=10000)
        self.logger.success("Successfully navigated to PIM section")

    def goto_admin(self):
        """Navigate to Admin section"""
        self.logger.step("Navigate to Admin section")
        self.page.wait_for_selector(self.admin_menu, timeout=10000)
        self.page.click(self.admin_menu)
        self.logger.success("Successfully navigated to Admin section")

    def goto_my_info(self):
        """Navigate to My Info section"""
        self.logger.step("Navigate to My Info section")
        self.page.wait_for_selector(self.my_info_menu, timeout=10000)
        self.page.click(self.my_info_menu)
        self.logger.success("Successfully navigated to My Info section")
