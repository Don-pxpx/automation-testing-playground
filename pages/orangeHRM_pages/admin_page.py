from helpers.log_helpers import InlineLogger

class AdminPage:
    def __init__(self, test):
        self.test = test
        self.logger = InlineLogger()
        
        # Admin menu locators
        self.job_menu = "a:contains('Job')"
        self.job_titles_menu = "a:contains('Job Titles')"
        self.job_categories_menu = "a:contains('Job Categories')"
        self.pay_grades_menu = "a:contains('Pay Grades')"
        self.employment_status_menu = "a:contains('Employment Status')"
        
        # Job Titles page locators
        self.add_job_title_button = "button:contains('Add')"
        self.job_title_name_field = "input[name='jobTitle'], input[placeholder*='Job Title'], input:first-of-type"
        self.job_description_field = "textarea[name='jobDescription'], textarea[placeholder*='Description'], textarea:first-of-type"
        self.job_specification_file_input = "input[type='file']"
        self.note_field = "textarea[name='note'], textarea[placeholder*='Note'], textarea:last-of-type"
        self.save_job_title_button = "button[type='submit']"
        self.cancel_job_title_button = "button:contains('Cancel')"
        
        # Job Titles list locators
        self.job_titles_table = "div.oxd-table-body"
        self.job_title_row = "div.oxd-table-row"
        self.edit_job_title_button = "button:contains('Edit')"
        self.delete_job_title_button = "button:contains('Delete')"
        self.confirm_delete_button = "button:contains('Yes, Delete')"

    def goto_job_titles(self):
        """Navigate to Job Titles section"""
        self.logger.step("Navigate to Job Titles section")
        # Navigate directly to the Job Titles page
        self.test.open("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewJobTitleList")
        self.test.wait_for_element_visible("h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module", timeout=10)
        self.logger.success("Successfully navigated to Job Titles section")

    def click_add_job_title(self):
        """Click the Add button to create a new job title"""
        self.logger.step("Click Add Job Title button")
        self.test.wait_for_element_visible(self.add_job_title_button, timeout=10)
        self.test.click(self.add_job_title_button)
        self.test.sleep(2)  # Wait for form to load
        # Try different field locators
        try:
            self.test.wait_for_element_visible(self.job_title_name_field, timeout=5)
        except:
            # Try alternative locators
            try:
                self.test.wait_for_element_visible("input[placeholder*='Job Title']", timeout=5)
            except:
                self.test.wait_for_element_visible("input", timeout=5)  # Any input field
        self.logger.success("Add Job Title form loaded")

    def fill_job_title_form(self, job_title, description="", note=""):
        """Fill the job title form with provided data"""
        self.logger.step(f"Fill job title form: {job_title}")
        
        # Fill job title name
        self.test.wait_for_element_visible(self.job_title_name_field, timeout=10)
        self.test.type(self.job_title_name_field, job_title)
        
        # Fill description if provided
        if description:
            self.test.type(self.job_description_field, description)
        
        # Fill note if provided
        if note:
            self.test.type(self.note_field, note)
        
        self.logger.success("Job title form filled successfully")

    def save_job_title(self):
        """Save the job title form"""
        self.logger.step("Save job title")
        self.test.wait_for_element_visible(self.save_job_title_button, timeout=10)
        self.test.click(self.save_job_title_button)
        self.test.sleep(2)  # Wait for save to complete
        self.logger.success("Job title saved successfully")

    def cancel_job_title(self):
        """Cancel the job title form"""
        self.logger.step("Cancel job title creation")
        self.test.wait_for_element_visible(self.cancel_job_title_button, timeout=10)
        self.test.click(self.cancel_job_title_button)
        self.logger.success("Job title creation cancelled")

    def search_job_title(self, job_title):
        """Search for a job title"""
        self.logger.step(f"Search for job title: {job_title}")
        # Try different search field locators
        search_field_selectors = [
            "input[placeholder='Search for Job Titles...']",
            "input[placeholder*='Search']",
            "input[placeholder*='job']",
            "input[placeholder*='title']",
            "input:first-of-type"
        ]
        
        search_field = None
        for selector in search_field_selectors:
            try:
                self.test.wait_for_element_visible(selector, timeout=3)
                search_field = selector
                break
            except:
                continue
        
        if search_field:
            self.test.type(search_field, job_title)
            self.test.click("button[type='submit']")
            self.logger.success(f"Searched for job title: {job_title}")
        else:
            self.logger.warning("Search field not found, skipping search")

    def edit_job_title(self, job_title, new_title, new_description=""):
        """Edit an existing job title"""
        self.logger.step(f"Edit job title: {job_title}")
        
        # Find and click edit button for the specific job title
        # This is a simplified approach - in a real scenario you'd need to find the specific row
        self.test.wait_for_element_visible(self.edit_job_title_button, timeout=10)
        self.test.click(self.edit_job_title_button)
        
        # Wait for edit form to load
        self.test.wait_for_element_visible(self.job_title_name_field, timeout=10)
        
        # Clear and fill the form
        self.test.clear(self.job_title_name_field)
        self.test.type(self.job_title_name_field, new_title)
        
        if new_description:
            self.test.clear(self.job_description_field)
            self.test.type(self.job_description_field, new_description)
        
        # Save changes
        self.test.click(self.save_job_title_button)
        self.test.sleep(2)
        self.logger.success(f"Job title updated to: {new_title}")

    def delete_job_title(self, job_title):
        """Delete a job title"""
        self.logger.step(f"Delete job title: {job_title}")
        
        # Find and click delete button for the specific job title
        self.test.wait_for_element_visible(self.delete_job_title_button, timeout=10)
        self.test.click(self.delete_job_title_button)
        
        # Confirm deletion
        self.test.wait_for_element_visible(self.confirm_delete_button, timeout=10)
        self.test.click(self.confirm_delete_button)
        self.test.sleep(2)
        self.logger.success(f"Job title deleted: {job_title}")

    def verify_job_title_exists(self, job_title):
        """Verify that a job title exists in the list"""
        self.logger.step(f"Verify job title exists: {job_title}")
        try:
            # Navigate back to the job titles list page
            self.test.open("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewJobTitleList")
            self.test.sleep(2)
            
            # Check if the job title appears in the results
            table_content = self.test.get_text(self.job_titles_table)
            if job_title in table_content:
                self.logger.success(f"Job title found: {job_title}")
                return True
            else:
                self.logger.warning(f"Job title not found in table: {job_title}")
                # Try searching
                try:
                    self.search_job_title(job_title)
                    table_content = self.test.get_text(self.job_titles_table)
                    if job_title in table_content:
                        self.logger.success(f"Job title found after search: {job_title}")
                        return True
                    else:
                        self.logger.error(f"Job title not found after search: {job_title}")
                        return False
                except:
                    self.logger.error(f"Search failed for job title: {job_title}")
                    return False
        except Exception as e:
            self.logger.error(f"Error verifying job title: {str(e)}")
            return False

    def get_job_titles_count(self):
        """Get the number of job titles in the list"""
        self.logger.step("Get job titles count")
        try:
            rows = self.test.find_elements(self.job_title_row)
            count = len(rows)
            self.logger.success(f"Found {count} job titles")
            return count
        except Exception as e:
            self.logger.error(f"Error getting job titles count: {str(e)}")
            return 0
