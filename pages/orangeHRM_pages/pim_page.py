from helpers.log_helpers import InlineLogger

class PimPage:
    def __init__(self, test):
        self.test = test
        self.logger = InlineLogger()
        # Locators - using more generic selectors since href might be dynamic
        self.add_employee_button = "a:contains('Add Employee')"
        self.employee_list_button = "a:contains('Employee List')"
        
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
        self.test.wait_for_element_visible(self.add_employee_button, timeout=10)
        self.test.click(self.add_employee_button)
        # Wait for add employee form to load
        self.test.wait_for_element_visible(self.first_name_field, timeout=10)
        self.logger.success("Add Employee form loaded")

    def click_employee_list(self):
        """Click the Employee List button"""
        self.logger.step("Click Employee List button")
        self.test.wait_for_element_visible(self.employee_list_button, timeout=10)
        self.test.click(self.employee_list_button)
        self.logger.success("Employee List page loaded")

    def fill_employee_form(self, first_name, middle_name, last_name):
        """Fill the employee form with basic information"""
        self.logger.step(f"Fill employee form: {first_name} {middle_name} {last_name}")
        
        # Fill first name
        self.test.wait_for_element_visible(self.first_name_field, timeout=10)
        self.test.type(self.first_name_field, first_name)
        
        # Fill middle name (if provided)
        if middle_name:
            self.test.type(self.middle_name_field, middle_name)
        
        # Fill last name
        self.test.type(self.last_name_field, last_name)
        
        self.logger.success("Employee form filled successfully")

    def set_employee_id(self, employee_id):
        """Set a custom employee ID"""
        self.logger.step(f"Set employee ID: {employee_id}")
        # Use JavaScript to find the employee ID field by looking for the field after "Employee Id" label
        js_script = """
        var labels = document.querySelectorAll('label');
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].textContent.includes('Employee Id')) {
                var parent = labels[i].closest('.oxd-input-group');
                var input = parent.querySelector('input');
                if (input) {
                    input.value = arguments[0];
                    return true;
                }
            }
        }
        return false;
        """
        result = self.test.execute_script(js_script, employee_id)
        if result:
            self.logger.success(f"Employee ID set to: {employee_id}")
        else:
            self.logger.error("Could not find employee ID field")

    def save_employee(self):
        """Save the employee form"""
        self.logger.step("Save employee information")
        self.test.click(self.save_button)
        # Wait for save to complete - the page might stay on add employee form
        self.test.sleep(3)
        self.logger.success("Employee saved successfully")

    def search_employee(self, employee_name):
        """Search for an employee by name"""
        self.logger.step(f"Search for employee: {employee_name}")
        self.test.wait_for_element_visible(self.search_employee_field, timeout=10)
        self.test.type(self.search_employee_field, employee_name)
        self.test.click(self.search_button)
        self.logger.success(f"Searched for employee: {employee_name}")

    def enable_login_details(self):
        """Enable create login details toggle"""
        self.logger.step("Enable create login details")
        self.test.click(self.create_login_details_toggle)
        self.logger.success("Login details creation enabled")
