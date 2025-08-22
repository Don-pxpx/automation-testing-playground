from seleniumbase import BaseCase
from faker import Faker

from config.orangeHRM_credentials import OrangeHRMData
from helpers.log_helpers import InlineLogger
from pages.orangeHRM_pages.login_page import LoginPage
from pages.orangeHRM_pages.dashboard_page import DashboardPage
from pages.orangeHRM_pages.pim_page import PimPage
from pages.orangeHRM_pages.employee_details_page import EmployeeDetailsPage

fake = Faker()

class AddEmployeeTests(BaseCase):

    def test_add_employee_random_and_with_custom_id(self):
        logger = InlineLogger()

        # 🔐 LOGIN (fresh session for reliability)
        logger.step("Open login and sign in")
        login = LoginPage(self)
        dash = DashboardPage(self)
        pim = PimPage(self)
        details = EmployeeDetailsPage(self)

        login.open_login()
        login.login(OrangeHRMData.USERNAME, OrangeHRMData.PASSWORD)
        self.assert_true(login.is_logged_in())
        logger.success("Logged in successfully")

        # ──────────────────────────────────────────────────────────────────
        # ➕ SCENARIO A: Add Employee (random data)
        # ──────────────────────────────────────────────────────────────────
        logger.step("Go to PIM and open Add Employee (Random Data)")
        dash.goto_pim()
        pim.click_add_employee()

        first_a = fake.first_name()
        middle_a = fake.first_name()
        last_a = fake.last_name()
        logger.note(f"Creating employee → {first_a} {middle_a} {last_a}")

        pim.fill_employee_form(first_a, middle_a, last_a)
        pim.save_employee()

        logger.step("Verify personal details for Random Data employee")
        details.wait_loaded()
        full_name_ui_a = details.get_full_name()
        self.assert_in(first_a, full_name_ui_a)
        self.assert_in(last_a, full_name_ui_a)
        logger.success(f"Random-data employee saved as: {full_name_ui_a}")

        # ──────────────────────────────────────────────────────────────────
        # ➕ SCENARIO B: Add Employee with custom Employee Id
        # (start from a clean entry point: back to PIM → Add Employee)
        # ──────────────────────────────────────────────────────────────────
        logger.step("Return to PIM and open Add Employee (Custom ID)")
        dash.goto_pim()
        pim.click_add_employee()

        first_b = fake.first_name()
        last_b = fake.last_name()
        custom_emp_id = str(fake.random_int(min=100000, max=999999))
        logger.note(f"Adding {first_b} {last_b} with Employee Id: {custom_emp_id}")

        pim.fill_employee_form(first_b, "", last_b)
        pim.set_employee_id(custom_emp_id)   # relies on your existing page method
        pim.save_employee()

        logger.step("Verify personal details for Custom ID employee")
        details.wait_loaded()
        full_name_ui_b = details.get_full_name()
        self.assert_in(first_b, full_name_ui_b)
        self.assert_in(last_b, full_name_ui_b)
        logger.success(f"Custom-ID employee saved as: {full_name_ui_b} (ID: {custom_emp_id})")
