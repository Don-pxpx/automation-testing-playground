from helpers.log_helpers import InlineLogger

class EmployeeDetailsPage:
    def __init__(self, test):
        self.test = test
        self.logger = InlineLogger()
        # Locators
        self.employee_name_header = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"
        self.personal_details_section = "div.orangehrm-edit-employee-content"
        self.first_name_value = "input[name='firstName']"
        self.middle_name_value = "input[name='middleName']"
        self.last_name_value = "input[name='lastName']"
        self.employee_id_value = "label:contains('Employee Id') + div span"
        self.edit_button = "button:contains('Edit')"
        self.save_button = "button[type='submit']"
        self.cancel_button = "button:contains('Cancel')"

    def wait_loaded(self):
        """Wait for employee details page to load"""
        self.logger.step("Wait for employee details page to load")
        # Since we're still on the add employee form, wait for the form to be ready
        self.test.wait_for_element_visible(self.first_name_value, timeout=15)
        self.logger.success("Employee details page loaded")

    def get_full_name(self):
        """Get the full name of the employee from the form fields"""
        self.logger.step("Get employee full name from form fields")
        first_name = self.get_first_name()
        middle_name = self.get_middle_name()
        last_name = self.get_last_name()
        
        # Construct full name
        full_name_parts = [first_name]
        if middle_name:
            full_name_parts.append(middle_name)
        full_name_parts.append(last_name)
        
        full_name = " ".join(full_name_parts)
        self.logger.success(f"Retrieved full name: {full_name}")
        return full_name

    def get_first_name(self):
        """Get the first name from the form"""
        self.logger.step("Get employee first name")
        self.test.wait_for_element_visible(self.first_name_value, timeout=10)
        first_name = self.test.get_attribute(self.first_name_value, "value")
        self.logger.success(f"Retrieved first name: {first_name}")
        return first_name

    def get_middle_name(self):
        """Get the middle name from the form"""
        self.logger.step("Get employee middle name")
        if self.test.is_element_visible(self.middle_name_value):
            middle_name = self.test.get_attribute(self.middle_name_value, "value")
            self.logger.success(f"Retrieved middle name: {middle_name}")
            return middle_name
        else:
            self.logger.note("No middle name found")
            return ""

    def get_last_name(self):
        """Get the last name from the form"""
        self.logger.step("Get employee last name")
        self.test.wait_for_element_visible(self.last_name_value, timeout=10)
        last_name = self.test.get_attribute(self.last_name_value, "value")
        self.logger.success(f"Retrieved last name: {last_name}")
        return last_name

    def get_employee_id(self):
        """Get the employee ID"""
        self.logger.step("Get employee ID")
        try:
            employee_id = self.test.get_text(self.employee_id_value)
            self.logger.success(f"Retrieved employee ID: {employee_id}")
            return employee_id
        except Exception:
            self.logger.note("Could not retrieve employee ID")
            return ""

    def click_edit(self):
        """Click the edit button to enable editing"""
        self.logger.step("Click edit button")
        self.test.wait_for_element_visible(self.edit_button, timeout=10)
        self.test.click(self.edit_button)
        self.logger.success("Edit mode enabled")

    def save_changes(self):
        """Save changes after editing"""
        self.logger.step("Save employee changes")
        self.test.wait_for_element_visible(self.save_button, timeout=10)
        self.test.click(self.save_button)
        self.logger.success("Changes saved successfully")

    def cancel_changes(self):
        """Cancel changes and return to view mode"""
        self.logger.step("Cancel employee changes")
        self.test.wait_for_element_visible(self.cancel_button, timeout=10)
        self.test.click(self.cancel_button)
        self.logger.success("Changes cancelled")

    def verify_employee_details(self, expected_first_name, expected_last_name):
        """Verify that employee details match expected values"""
        self.logger.step("Verify employee details")
        actual_first_name = self.get_first_name()
        actual_last_name = self.get_last_name()
        
        if actual_first_name == expected_first_name and actual_last_name == expected_last_name:
            self.logger.success(f"Employee details verified: {actual_first_name} {actual_last_name}")
            return True
        else:
            self.logger.error(f"Employee details mismatch. Expected: {expected_first_name} {expected_last_name}, Got: {actual_first_name} {actual_last_name}")
            return False
