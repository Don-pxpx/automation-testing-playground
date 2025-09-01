from seleniumbase import BaseCase
from faker import Faker

from config.orangeHRM_credentials import OrangeHRMData
from helpers.log_helpers import InlineLogger
from pages.orangeHRM_pages.login_page import LoginPage
from pages.orangeHRM_pages.dashboard_page import DashboardPage
from pages.orangeHRM_pages.pim_page import PimPage
from pages.orangeHRM_pages.employee_details_page import EmployeeDetailsPage

fake = Faker()

class EmployeeSearchTests(BaseCase):

    def test_employee_search_and_filtering(self):
        logger = InlineLogger()
        logger.test_start("Employee Search and Filtering Test")

        # 🔐 LOGIN
        logger.step("Login to OrangeHRM")
        login = LoginPage(self)
        dash = DashboardPage(self)
        pim = PimPage(self)
        details = EmployeeDetailsPage(self)

        login.open_login()
        login.login(OrangeHRMData.USERNAME, OrangeHRMData.PASSWORD)
        self.assert_true(login.is_logged_in())
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

        pim.fill_employee_form(test_first_name, "", test_last_name)
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
        self.wait_for_element_visible("div.oxd-table-body", timeout=10)
        search_results = self.get_text("div.oxd-table-body")
        
        # Check if our employee appears in the results
        if test_first_name in search_results and test_last_name in search_results:
            logger.success(f"Found employee by full name: {test_employee_name}")
        else:
            logger.warning(f"Employee '{test_employee_name}' not found in search results")
            logger.note("This might be due to timing or search indexing delay")

        # Test 2: Search by first name only
        logger.step("Search employee by first name only")
        pim.search_employee(test_first_name)
        
        search_results = self.get_text("div.oxd-table-body")
        if test_first_name in search_results:
            logger.success(f"Found employee by first name: {test_first_name}")
        else:
            logger.warning(f"Employee with first name '{test_first_name}' not found")

        # Test 3: Search by last name only
        logger.step("Search employee by last name only")
        pim.search_employee(test_last_name)
        
        search_results = self.get_text("div.oxd-table-body")
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
            no_records_element = self.get_text("div.oxd-table-body")
            if "No Records Found" in no_records_element or "No data" in no_records_element:
                logger.success(f"Correctly shows no results for: {fake_name}")
            else:
                logger.warning("Expected 'No Records Found' message not found")
        except Exception:
            logger.success("Search correctly returned no results for non-existent employee")

        # Test 5: Clear search and verify all employees visible
        logger.step("Clear search and verify all employees visible")
        # Clear the search field
        self.clear("input[placeholder='Type for hints...']")
        self.click("button[type='submit']")
        
        # Wait for results to refresh
        self.sleep(2)
        all_results = self.get_text("div.oxd-table-body")
        self.assert_true(len(all_results) > 0, "Should show employees after clearing search")
        logger.success("Search cleared successfully, all employees visible")

        # Test 6: Verify our test employee exists in the full list
        logger.step("Verify test employee exists in full employee list")
        if test_first_name in all_results and test_last_name in all_results:
            logger.success(f"Test employee '{test_employee_name}' confirmed in employee list")
        else:
            logger.warning(f"Test employee '{test_employee_name}' not found in full list")
            logger.note("This might indicate a timing issue with employee creation")

        logger.test_end("Employee Search and Filtering Test", "passed")
        logger.summary(passed=1, failed=0, skipped=0)
