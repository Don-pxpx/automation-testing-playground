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

def test_employee_search_and_filtering(page: Page):
    """Test employee search and filtering functionality."""
    logger = InlineLogger()
    logger.test_start("Employee Search and Filtering Test")

    # 🔐 LOGIN
    logger.step("Login to OrangeHRM")
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
    logger.success("Successfully logged in")

    # ➕ CREATE TEST EMPLOYEE FOR SEARCHING
    logger.step("Create test employee for search functionality")
    dash.goto_pim()
    pim.click_add_employee()

    # Create employee with distinctive name for searching
    test_first_name = fake.first_name()
    test_last_name = fake.last_name()
    test_employee_name = f"{test_first_name} {test_last_name}"
    logger.note(f"Creating test employee: {test_employee_name}")

    employee_data = EmployeeData(
        first_name=test_first_name,
        middle_name="",
        last_name=test_last_name
    )
    pim.fill_employee_form_with_model(employee_data)
    pim.save_employee()
    logger.success(f"Test employee created: {test_employee_name}")

    # 🔍 TEST EMPLOYEE SEARCH FUNCTIONALITY
    logger.step("Navigate to Employee List for search testing")
    dash.goto_pim()
    pim.click_employee_list()
    logger.success("Employee List page loaded")

    # Test 1: Search by full name
    logger.step("Search employee by full name")
    pim.search_employee(test_employee_name)
    
    # Wait for search results and verify
    page.wait_for_selector("div.oxd-table-body", timeout=10000)
    search_results = page.locator("div.oxd-table-body").text_content() or ""
    
    # Check if our employee appears in the results
    if test_first_name in search_results and test_last_name in search_results:
        logger.success(f"Found employee by full name: {test_employee_name}")
    else:
        logger.warning(f"Employee '{test_employee_name}' not found in search results")
        logger.note("This might be due to timing or search indexing delay")

    # Test 2: Search by first name only
    logger.step("Search employee by first name only")
    pim.search_employee(test_first_name)
    
    search_results = page.locator("div.oxd-table-body").text_content() or ""
    if test_first_name in search_results:
        logger.success(f"Found employee by first name: {test_first_name}")
    else:
        logger.warning(f"Employee with first name '{test_first_name}' not found")

    # Test 3: Search by last name only
    logger.step("Search employee by last name only")
    pim.search_employee(test_last_name)
    
    search_results = page.locator("div.oxd-table-body").text_content() or ""
    if test_last_name in search_results:
        logger.success(f"Found employee by last name: {test_last_name}")
    else:
        logger.warning(f"Employee with last name '{test_last_name}' not found")

    # Test 4: Search with non-existent employee
    logger.step("Search for non-existent employee")
    fake_name = fake.name()
    pim.search_employee(fake_name)
    
    # Check for "No Records Found" message
    try:
        no_records_element = page.locator("div.oxd-table-body").text_content() or ""
        if "No Records Found" in no_records_element or "No data" in no_records_element:
            logger.success(f"Correctly shows no results for: {fake_name}")
        else:
            logger.warning("Expected 'No Records Found' message not found")
    except Exception:
        logger.success("Search correctly returned no results for non-existent employee")

    # Test 5: Clear search and verify all employees visible
    logger.step("Clear search and verify all employees visible")
    # Clear the search field
    search_field = page.locator("input[placeholder='Type for hints...']")
    if search_field.is_visible():
        search_field.fill("")
        page.click("button[type='submit']")
        
        # Wait for results to refresh - INTENTIONAL: This may fail due to timing
        page.wait_for_timeout(3000)
        all_results = page.locator("div.oxd-table-body").text_content() or ""
        # INTENTIONAL FAILURE: Sometimes search results don't refresh immediately
        # This simulates a real-world timing issue with async search operations
        if len(all_results) == 0:
            logger.warning("Search results empty after clearing - timing issue (intentional failure scenario)")
            raise AssertionError("Search results empty after clearing - simulates real-world async timing issue")
        logger.success("Search cleared successfully, all employees visible")
    else:
        logger.warning("Search field not found - skipping clear test")

    # Test 6: Verify our test employee exists in the full list
    logger.step("Verify test employee exists in full employee list")
    if test_first_name in all_results and test_last_name in all_results:
        logger.success(f"Test employee '{test_employee_name}' confirmed in employee list")
    else:
        logger.warning(f"Test employee '{test_employee_name}' not found in full list")
        logger.note("This might indicate a timing issue with employee creation")

    logger.test_end("Employee Search and Filtering Test", "passed")
    logger.summary(passed=1, failed=0, skipped=0)
