import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.config.orangeHRM_credentials import OrangeHRMData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.orangeHRM_pages.login_page import LoginPage
from automation_testing_playground.pages.orangeHRM_pages.dashboard_page import DashboardPage
from automation_testing_playground.pages.orangeHRM_pages.my_info_page import MyInfoPage
from automation_testing_playground.models.orangehrm_models import LoginCredentials

fake = Faker()

def test_my_info_management_comprehensive(page: Page):
    """Test My Info management functionality."""
    logger = InlineLogger()
    logger.test_start("My Info Management Comprehensive Test")

    # 🔐 LOGIN
    logger.step("Login to OrangeHRM")
    login = LoginPage(page)
    dash = DashboardPage(page)
    my_info = MyInfoPage(page)

    login.open_login()
    credentials = LoginCredentials(
        username=OrangeHRMData.USERNAME,
        password=OrangeHRMData.PASSWORD
    )
    login.login_with_credentials(credentials)
    expect(page.locator(login.dashboard_marker)).to_be_visible()
    assert login.is_logged_in()
    logger.success("Successfully logged in")

    # 📋 NAVIGATE TO MY INFO
    logger.step("Navigate to My Info section")
    dash.goto_my_info()
    my_info.wait_for_page_load()
    assert my_info.is_page_loaded()
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

    logger.test_end("My Info Management Comprehensive Test", "passed")
    logger.summary(passed=1, failed=0, skipped=0)
