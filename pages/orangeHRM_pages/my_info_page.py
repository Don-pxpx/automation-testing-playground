from helpers.log_helpers import InlineLogger

class MyInfoPage:
    def __init__(self, test):
        self.test = test
        self.logger = InlineLogger()
        
        # Page markers
        self.personal_details_title = "h6.orangehrm-main-title"
        self.breadcrumb = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"
        
        # Form fields - Personal Details
        self.first_name_field = "input[name='firstName']"
        self.middle_name_field = "input[name='middleName']"
        self.last_name_field = "input[name='lastName']"
        self.employee_id_field = "input[name='employeeId']"
        self.other_id_field = "input[name='otherId']"
        self.driver_license_field = "input[name='licenseNo']"
        self.ssn_field = "input[name='ssnNumber']"
        self.sin_field = "input[name='sinNumber']"
        
        # Date fields
        self.birth_date_field = "input[placeholder='yyyy-mm-dd']"
        self.license_expiry_field = "input[placeholder='yyyy-mm-dd']"
        
        # Buttons
        self.save_button = "button[type='submit']"
        self.cancel_button = "button:contains('Cancel')"
        self.edit_button = "button:contains('Edit')"
        
        # Gender radio buttons
        self.male_radio = "input[value='1']"
        self.female_radio = "input[value='2']"
        
        # Marital status dropdown
        self.marital_status_dropdown = "div.oxd-select-wrapper"
        
        # Nationality dropdown
        self.nationality_dropdown = "div.oxd-select-wrapper"

    def wait_for_page_load(self):
        """Wait for My Info page to load"""
        self.logger.step("Wait for My Info page to load")
        self.test.wait_for_element_visible(self.personal_details_title, timeout=15)
        self.logger.success("My Info page loaded successfully")

    def is_page_loaded(self):
        """Check if My Info page is loaded"""
        return self.test.is_element_visible(self.personal_details_title)

    def get_current_personal_info(self):
        """Get current personal information from form fields"""
        self.logger.step("Get current personal information")
        
        info = {}
        try:
            # Only get fields that we know exist
            info['first_name'] = self.test.get_value(self.first_name_field)
            info['middle_name'] = self.test.get_value(self.middle_name_field)
            info['last_name'] = self.test.get_value(self.last_name_field)
            
            # Try to get employee ID if it exists
            try:
                info['employee_id'] = self.test.get_value(self.employee_id_field)
            except:
                info['employee_id'] = ""
            
            self.logger.success("Retrieved current personal information")
            return info
        except Exception as e:
            self.logger.error(f"Error getting personal info: {str(e)}")
            return {}

    def edit_personal_info(self, first_name=None, middle_name=None, last_name=None):
        """Edit personal information fields"""
        self.logger.step("Edit personal information")
        
        if first_name:
            self.test.clear(self.first_name_field)
            self.test.type(self.first_name_field, first_name)
            self.logger.note(f"Set first name: {first_name}")
        
        if middle_name:
            self.test.clear(self.middle_name_field)
            self.test.type(self.middle_name_field, middle_name)
            self.logger.note(f"Set middle name: {middle_name}")
        
        if last_name:
            self.test.clear(self.last_name_field)
            self.test.type(self.last_name_field, last_name)
            self.logger.note(f"Set last name: {last_name}")
        
        self.logger.success("Personal information edited")

    def save_changes(self):
        """Save the changes made to personal information"""
        self.logger.step("Save personal information changes")
        self.test.wait_for_element_visible(self.save_button, timeout=10)
        self.test.click(self.save_button)
        self.test.sleep(2)  # Wait for save to complete
        self.logger.success("Personal information saved successfully")

    def cancel_changes(self):
        """Cancel the changes made to personal information"""
        self.logger.step("Cancel personal information changes")
        self.test.wait_for_element_visible(self.cancel_button, timeout=10)
        self.test.click(self.cancel_button)
        self.logger.success("Personal information changes cancelled")

    def set_gender(self, gender):
        """Set gender (male/female)"""
        self.logger.step(f"Set gender to: {gender}")
        
        if gender.lower() == 'male':
            self.test.click(self.male_radio)
        elif gender.lower() == 'female':
            self.test.click(self.female_radio)
        else:
            self.logger.warning(f"Invalid gender: {gender}")
            return
        
        self.logger.success(f"Gender set to: {gender}")

    def set_marital_status(self, status):
        """Set marital status"""
        self.logger.step(f"Set marital status to: {status}")
        
        # Click on marital status dropdown
        self.test.click(self.marital_status_dropdown)
        self.test.sleep(1)
        
        # Select the option
        option_selector = f"div.oxd-select-option:contains('{status}')"
        self.test.click(option_selector)
        self.logger.success(f"Marital status set to: {status}")

    def set_nationality(self, nationality):
        """Set nationality"""
        self.logger.step(f"Set nationality to: {nationality}")
        
        # Click on nationality dropdown
        self.test.click(self.nationality_dropdown)
        self.test.sleep(1)
        
        # Select the option
        option_selector = f"div.oxd-select-option:contains('{nationality}')"
        self.test.click(option_selector)
        self.logger.success(f"Nationality set to: {nationality}")

    def set_birth_date(self, date):
        """Set birth date (format: yyyy-mm-dd)"""
        self.logger.step(f"Set birth date to: {date}")
        self.test.clear(self.birth_date_field)
        self.test.type(self.birth_date_field, date)
        self.logger.success(f"Birth date set to: {date}")

    def set_license_expiry(self, date):
        """Set license expiry date (format: yyyy-mm-dd)"""
        self.logger.step(f"Set license expiry to: {date}")
        self.test.clear(self.license_expiry_field)
        self.test.type(self.license_expiry_field, date)
        self.logger.success(f"License expiry set to: {date}")

    def verify_changes_saved(self, expected_info):
        """Verify that changes were saved correctly"""
        self.logger.step("Verify changes were saved")
        
        current_info = self.get_current_personal_info()
        
        for field, expected_value in expected_info.items():
            if field in current_info:
                actual_value = current_info[field]
                if actual_value == expected_value:
                    self.logger.success(f"✓ {field}: {expected_value}")
                else:
                    self.logger.error(f"✗ {field}: expected '{expected_value}', got '{actual_value}'")
            else:
                self.logger.warning(f"Field '{field}' not found in current info")

    def get_full_name(self):
        """Get the full name from the form"""
        self.logger.step("Get full name from form")
        
        first_name = self.test.get_value(self.first_name_field) or ""
        middle_name = self.test.get_value(self.middle_name_field) or ""
        last_name = self.test.get_value(self.last_name_field) or ""
        
        name_parts = [first_name]
        if middle_name:
            name_parts.append(middle_name)
        name_parts.append(last_name)
        
        full_name = " ".join(name_parts).strip()
        self.logger.success(f"Full name: {full_name}")
        return full_name
