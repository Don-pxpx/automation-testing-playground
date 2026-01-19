from playwright.sync_api import Page
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.orangehrm_models import EmployeeData

class PimPage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object
        self.logger = InlineLogger()
        # Locators - using more generic selectors since href might be dynamic
        self.add_employee_button = "text=Add Employee"
        self.employee_list_button = "text=Employee List"
        
        # Add Employee Form Locators
        self.first_name_field = "input[name='firstName']"
        self.middle_name_field = "input[name='middleName']"
        self.last_name_field = "input[name='lastName']"
        self.employee_id_field = "input[value*='0']"  # Employee ID field has a numeric value
        self.save_button = "button[type='submit']"
        self.create_login_details_toggle = "span.oxd-switch-input.oxd-switch-input--active"
        
        # Employee List Locators
        self.search_employee_field = "input[placeholder='Type for hints...']"
        self.search_button = "button[type='submit']"

    def click_add_employee(self):
        """Click the Add Employee button"""
        self.logger.step("Click Add Employee button")
        self.page.wait_for_selector(self.add_employee_button, timeout=10000)
        self.page.click(self.add_employee_button)
        # Wait for add employee form to load
        self.page.wait_for_selector(self.first_name_field, timeout=10000)
        self.logger.success("Add Employee form loaded")

    def click_employee_list(self):
        """Click the Employee List button"""
        self.logger.step("Click Employee List button")
        self.page.wait_for_selector(self.employee_list_button, timeout=10000)
        self.page.click(self.employee_list_button)
        self.logger.success("Employee List page loaded")

    def fill_employee_form(self, first_name: str, middle_name: str, last_name: str):
        """Fill the employee form with basic information"""
        self.logger.step(f"Fill employee form: {first_name} {middle_name} {last_name}")
        
        # Fill first name
        self.page.wait_for_selector(self.first_name_field, timeout=10000)
        self.page.fill(self.first_name_field, first_name)
        
        # Fill middle name (if provided)
        if middle_name:
            self.page.fill(self.middle_name_field, middle_name)
        
        # Fill last name
        self.page.fill(self.last_name_field, last_name)
        
        self.logger.success("Employee form filled successfully")

    def fill_employee_form_with_model(self, employee_data: EmployeeData):
        """Fill employee form using Pydantic model."""
        self.fill_employee_form(
            employee_data.first_name,
            employee_data.middle_name or "",
            employee_data.last_name
        )
        if employee_data.employee_id:
            self.set_employee_id(employee_data.employee_id)

    def set_employee_id(self, employee_id: str):
        """Set a custom employee ID"""
        self.logger.step(f"Set employee ID: {employee_id}")
        # Use JavaScript to find the employee ID field by looking for the field after "Employee Id" label
        js_script = """
        (function(empId) {
            var labels = document.querySelectorAll('label');
            for (var i = 0; i < labels.length; i++) {
                if (labels[i].textContent.includes('Employee Id')) {
                    var parent = labels[i].closest('.oxd-input-group');
                    var input = parent.querySelector('input');
                    if (input) {
                        input.value = empId;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        return true;
                    }
                }
            }
            return false;
        })
        """
        result = self.page.evaluate(js_script, employee_id)
        if result:
            self.logger.success(f"Employee ID set to: {employee_id}")
        else:
            self.logger.error("Could not find employee ID field")

    def save_employee(self):
        """Save the employee form"""
        self.logger.step("Save employee information")
        self.page.click(self.save_button)
        # Wait for save to complete - the page might stay on add employee form
        self.page.wait_for_timeout(3000)
        self.logger.success("Employee saved successfully")

    def search_employee(self, employee_name: str):
        """Search for an employee by name"""
        self.logger.step(f"Search for employee: {employee_name}")
        self.page.wait_for_selector(self.search_employee_field, timeout=10000)
        self.page.fill(self.search_employee_field, employee_name)
        self.page.click(self.search_button)
        self.logger.success(f"Searched for employee: {employee_name}")

    def enable_login_details(self):
        """Enable create login details toggle"""
        self.logger.step("Enable create login details")
        self.page.click(self.create_login_details_toggle)
        self.logger.success("Login details creation enabled")
