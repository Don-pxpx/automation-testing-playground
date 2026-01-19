from playwright.sync_api import Page
from automation_testing_playground.helpers.log_helpers import InlineLogger

class MyInfoPage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object
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
        self.cancel_button = "button:has-text('Cancel')"
        self.edit_button = "button:has-text('Edit')"
        
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
        self.page.wait_for_selector(self.personal_details_title, timeout=15000)
        self.logger.success("My Info page loaded successfully")

    def is_page_loaded(self) -> bool:
        """Check if My Info page is loaded"""
        # Use first() to handle multiple elements with same class
        return self.page.locator(self.personal_details_title).first.is_visible()

    def get_current_personal_info(self) -> dict[str, str]:
        """Get current personal information from form fields"""
        self.logger.step("Get current personal information")
        
        info = {}
        try:
            # Only get fields that we know exist
            info['first_name'] = self.page.locator(self.first_name_field).input_value()
            info['middle_name'] = self.page.locator(self.middle_name_field).input_value()
            info['last_name'] = self.page.locator(self.last_name_field).input_value()
            
            # Try to get employee ID if it exists
            try:
                info['employee_id'] = self.page.locator(self.employee_id_field).input_value()
            except:
                info['employee_id'] = ""
            
            self.logger.success("Retrieved current personal information")
            return info
        except Exception as e:
            self.logger.error(f"Error getting personal info: {str(e)}")
            return {}

    def edit_personal_info(self, first_name: str | None = None, middle_name: str | None = None, last_name: str | None = None):
        """Edit personal information fields"""
        self.logger.step("Edit personal information")
        
        if first_name:
            self.page.fill(self.first_name_field, first_name)
            self.logger.note(f"Set first name: {first_name}")
        
        if middle_name:
            self.page.fill(self.middle_name_field, middle_name)
            self.logger.note(f"Set middle name: {middle_name}")
        
        if last_name:
            self.page.fill(self.last_name_field, last_name)
            self.logger.note(f"Set last name: {last_name}")
        
        self.logger.success("Personal information edited")

    def save_changes(self):
        """Save the changes made to personal information"""
        self.logger.step("Save personal information changes")
        self.page.wait_for_selector(self.save_button, timeout=10000)
        self.page.click(self.save_button)
        self.page.wait_for_timeout(2000)  # Wait for save to complete
        self.logger.success("Personal information saved successfully")

    def cancel_changes(self):
        """Cancel the changes made to personal information"""
        self.logger.step("Cancel personal information changes")
        self.page.wait_for_selector(self.cancel_button, timeout=10000)
        self.page.click(self.cancel_button)
        self.logger.success("Personal information changes cancelled")

    def set_gender(self, gender: str):
        """Set gender (male/female)"""
        self.logger.step(f"Set gender to: {gender}")
        
        if gender.lower() == 'male':
            self.page.click(self.male_radio)
        elif gender.lower() == 'female':
            self.page.click(self.female_radio)
        else:
            self.logger.warning(f"Invalid gender: {gender}")
            return
        
        self.logger.success(f"Gender set to: {gender}")

    def set_marital_status(self, status: str):
        """Set marital status"""
        self.logger.step(f"Set marital status to: {status}")
        
        # Click on marital status dropdown
        self.page.click(self.marital_status_dropdown)
        self.page.wait_for_timeout(1000)
        
        # Select the option
        option_selector = f"div.oxd-select-option:has-text('{status}')"
        self.page.click(option_selector)
        self.logger.success(f"Marital status set to: {status}")

    def set_nationality(self, nationality: str):
        """Set nationality"""
        self.logger.step(f"Set nationality to: {nationality}")
        
        # Click on nationality dropdown
        self.page.click(self.nationality_dropdown)
        self.page.wait_for_timeout(1000)
        
        # Select the option
        option_selector = f"div.oxd-select-option:has-text('{nationality}')"
        self.page.click(option_selector)
        self.logger.success(f"Nationality set to: {nationality}")

    def set_birth_date(self, date: str):
        """Set birth date (format: yyyy-mm-dd)"""
        self.logger.step(f"Set birth date to: {date}")
        self.page.fill(self.birth_date_field, date)
        self.logger.success(f"Birth date set to: {date}")

    def set_license_expiry(self, date: str):
        """Set license expiry date (format: yyyy-mm-dd)"""
        self.logger.step(f"Set license expiry to: {date}")
        self.page.fill(self.license_expiry_field, date)
        self.logger.success(f"License expiry set to: {date}")

    def verify_changes_saved(self, expected_info: dict[str, str]):
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

    def get_full_name(self) -> str:
        """Get the full name from the form"""
        self.logger.step("Get full name from form")
        
        first_name = self.page.locator(self.first_name_field).input_value() or ""
        middle_name = self.page.locator(self.middle_name_field).input_value() or ""
        last_name = self.page.locator(self.last_name_field).input_value() or ""
        
        name_parts = [first_name]
        if middle_name:
            name_parts.append(middle_name)
        name_parts.append(last_name)
        
        full_name = " ".join(name_parts).strip()
        self.logger.success(f"Full name: {full_name}")
        return full_name
