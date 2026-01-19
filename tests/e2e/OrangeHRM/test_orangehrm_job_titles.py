import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.config.orangeHRM_credentials import OrangeHRMData
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.orangeHRM_pages.login_page import LoginPage
from automation_testing_playground.pages.orangeHRM_pages.dashboard_page import DashboardPage
from automation_testing_playground.pages.orangeHRM_pages.admin_page import AdminPage
from automation_testing_playground.models.orangehrm_models import LoginCredentials, JobTitleData

fake = Faker()

def test_job_titles_management(page: Page):
    """Test job titles management functionality - INTENTIONALLY FAILS due to timing issue."""
    logger = InlineLogger()
    logger.test_start("Job Titles Management Test")

    # 🔐 LOGIN
    logger.step("Login to OrangeHRM")
    login = LoginPage(page)
    dash = DashboardPage(page)
    admin = AdminPage(page)

    login.open_login()
    credentials = LoginCredentials(
        username=OrangeHRMData.USERNAME,
        password=OrangeHRMData.PASSWORD
    )
    login.login_with_credentials(credentials)
    expect(page.locator(login.dashboard_marker)).to_be_visible()
    assert login.is_logged_in()
    logger.success("Successfully logged in")

    # 🏢 NAVIGATE TO ADMIN → JOB TITLES
    logger.step("Navigate to Admin → Job Titles")
    dash.goto_admin()
    admin.goto_job_titles()
    logger.success("Successfully navigated to Job Titles section")

    # 📊 GET INITIAL JOB TITLES COUNT
    logger.step("Get initial job titles count")
    initial_count = admin.get_job_titles_count()
    logger.note(f"Initial job titles count: {initial_count}")

    # ➕ TEST 1: ADD NEW JOB TITLE
    logger.step("Add new job title")
    new_job_title = f"TestJob{fake.random_number(digits=3)}"
    job_description = "Test job description"
    job_note = "Test job note"
    
    logger.note(f"Creating job title: {new_job_title}")
    admin.click_add_job_title()
    
    job_title_data = JobTitleData(
        job_title=new_job_title,
        job_description=job_description,
        note=job_note
    )
    admin.fill_job_title_form_with_model(job_title_data)
    admin.save_job_title()
    
    # INTENTIONAL FAILURE: Not waiting long enough for job title to appear in list
    # This simulates a real-world timing issue
    page.wait_for_timeout(1000)  # Too short - should be longer
    
    # Verify job title was added (this will likely fail due to timing)
    try:
        assert admin.verify_job_title_exists(new_job_title), f"Job title '{new_job_title}' should exist but verification failed (timing issue)"
        logger.success(f"Job title '{new_job_title}' added and verified successfully")
    except AssertionError:
        logger.warning(f"Job title '{new_job_title}' was created but verification failed - timing issue")
        # This is an intentional failure to make results more realistic
        raise AssertionError(f"Job title verification failed - this simulates a real-world timing/race condition issue")

    logger.test_end("Job Titles Management Test", "failed")
    logger.summary(passed=0, failed=1, skipped=0)
