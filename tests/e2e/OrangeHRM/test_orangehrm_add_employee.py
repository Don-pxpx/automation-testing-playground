import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.config.orangeHRM_credentials import OrangeHRMData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.orangeHRM_pages.login_page import LoginPage
from automation_testing_playground.pages.orangeHRM_pages.dashboard_page import DashboardPage
from automation_testing_playground.pages.orangeHRM_pages.pim_page import PimPage
from automation_testing_playground.pages.orangeHRM_pages.employee_details_page import EmployeeDetailsPage
from automation_testing_playground.models.orangehrm_models import LoginCredentials, EmployeeData

fake = Faker()

def test_add_employee_random_and_with_custom_id(page: Page):
    """Test adding employee with random data and custom employee ID."""
    logger = InlineLogger()

    # 🔐 LOGIN (fresh session for reliability)
    logger.step("Open login and sign in")
    login = LoginPage(page)
    dash = DashboardPage(page)
    pim = PimPage(page)
    details = EmployeeDetailsPage(page)

    login.open_login()
    credentials = LoginCredentials(
        username=OrangeHRMData.USERNAME,
        password=OrangeHRMData.PASSWORD
    )
    login.login_with_credentials(credentials)
    expect(page.locator(login.dashboard_marker)).to_be_visible()
    assert login.is_logged_in()
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

    employee_data_a = EmployeeData(
        first_name=first_a,
        middle_name=middle_a,
        last_name=last_a
    )
    pim.fill_employee_form_with_model(employee_data_a)
    pim.save_employee()

    logger.step("Verify personal details for Random Data employee")
    details.wait_loaded()
    full_name_ui_a = details.get_full_name()
    assert first_a in full_name_ui_a
    assert last_a in full_name_ui_a
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

    employee_data_b = EmployeeData(
        first_name=first_b,
        middle_name="",
        last_name=last_b,
        employee_id=custom_emp_id
    )
    pim.fill_employee_form_with_model(employee_data_b)
    pim.save_employee()

    logger.step("Verify personal details for Custom ID employee")
    details.wait_loaded()
    full_name_ui_b = details.get_full_name()
    assert first_b in full_name_ui_b
    assert last_b in full_name_ui_b
    logger.success(f"Custom-ID employee saved as: {full_name_ui_b} (ID: {custom_emp_id})")
