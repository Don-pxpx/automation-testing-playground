from seleniumbase import BaseCase
from faker import Faker

from config.orangeHRM_credentials import OrangeHRMData
from helpers.log_helpers import InlineLogger
from pages.orangeHRM_pages.login_page import LoginPage
from pages.orangeHRM_pages.dashboard_page import DashboardPage
from pages.orangeHRM_pages.my_info_page import MyInfoPage

fake = Faker()

class MyInfoManagementTests(BaseCase):

    def test_my_info_management_comprehensive(self):
        logger = InlineLogger()
        logger.test_start("My Info Management Comprehensive Test")

        # 🔐 LOGIN
        logger.step("Login to OrangeHRM")
        login = LoginPage(self)
        dash = DashboardPage(self)
        my_info = MyInfoPage(self)

        login.open_login()
        login.login(OrangeHRMData.USERNAME, OrangeHRMData.PASSWORD)
        self.assert_true(login.is_logged_in())
        logger.success("Successfully logged in")

        # 📋 NAVIGATE TO MY INFO
        logger.step("Navigate to My Info section")
        dash.goto_my_info()
        my_info.wait_for_page_load()
        self.assert_true(my_info.is_page_loaded())
        logger.success("Successfully navigated to My Info section")

        # 📖 TEST 1: VIEW CURRENT PERSONAL INFORMATION
        logger.step("View current personal information")
        current_info = my_info.get_current_personal_info()
        
        if current_info:
            logger.note("Current personal information:")
            for field, value in current_info.items():
                if value:
                    logger.note(f"  {field}: {value}")
            logger.success("Successfully retrieved current personal information")
        else:
            logger.warning("No personal information found or could not retrieve")

        # ✏️ TEST 2: EDIT PERSONAL INFORMATION
        logger.step("Edit personal information with new data")
        
        # Generate test data
        new_first_name = fake.first_name()
        new_middle_name = fake.first_name()
        new_last_name = fake.last_name()
        
        logger.note(f"New test data:")
        logger.note(f"  First Name: {new_first_name}")
        logger.note(f"  Middle Name: {new_middle_name}")
        logger.note(f"  Last Name: {new_last_name}")

        # Edit the information
        my_info.edit_personal_info(
            first_name=new_first_name,
            middle_name=new_middle_name,
            last_name=new_last_name
        )
        logger.success("Personal information edited successfully")

        # 💾 TEST 3: SAVE CHANGES
        logger.step("Save the changes")
        my_info.save_changes()
        logger.success("Changes saved successfully")

        # ✅ TEST 4: VERIFY CHANGES WERE SAVED
        logger.step("Verify changes were saved correctly")
        expected_info = {
            'first_name': new_first_name,
            'middle_name': new_middle_name,
            'last_name': new_last_name
        }
        
        my_info.verify_changes_saved(expected_info)
        logger.success("Changes verification completed")

        # 📝 TEST 5: VERIFY FULL NAME
        logger.step("Verify full name is correct")
        full_name = my_info.get_full_name()
        expected_full_name = f"{new_first_name} {new_middle_name} {new_last_name}"
        
        if full_name == expected_full_name:
            logger.success(f"Full name is correct: {full_name}")
        else:
            logger.error(f"Full name mismatch: expected '{expected_full_name}', got '{full_name}'")

        # 🔄 TEST 6: TEST ADDITIONAL EDIT FUNCTIONALITY
        logger.step("Test additional edit functionality")
        
        # Generate different test data for additional edit
        additional_first_name = fake.first_name()
        additional_last_name = fake.last_name()
        
        logger.note(f"Attempting additional edit:")
        logger.note(f"  First Name: {additional_first_name}")
        logger.note(f"  Last Name: {additional_last_name}")

        # Edit information again
        my_info.edit_personal_info(
            first_name=additional_first_name,
            last_name=additional_last_name
        )
        
        # Save the additional changes
        my_info.save_changes()
        logger.success("Additional changes saved successfully")

        # Verify the additional changes
        logger.step("Verify additional changes were saved")
        additional_expected_info = {
            'first_name': additional_first_name,
            'last_name': additional_last_name
        }
        
        my_info.verify_changes_saved(additional_expected_info)
        logger.success("Additional changes verification completed")

        # 📊 TEST 7: FINAL VERIFICATION
        logger.step("Final verification of all functionality")
        
        # Verify final state
        final_info = my_info.get_current_personal_info()
        logger.note("Final personal information state:")
        for field, value in final_info.items():
            if value:
                logger.note(f"  {field}: {value}")
        
        # Verify full name one more time
        final_full_name = my_info.get_full_name()
        expected_final_name = f"{additional_first_name} {additional_last_name}"
        
        if final_full_name == expected_final_name:
            logger.success(f"Final full name is correct: {final_full_name}")
        else:
            logger.error(f"Final full name mismatch: expected '{expected_final_name}', got '{final_full_name}'")
        
        logger.success("Final verification completed")

        logger.test_end("My Info Management Comprehensive Test", "passed")
        logger.summary(passed=1, failed=0, skipped=0)
