"""
BlazeDemo Form Validation Tests

This module contains test cases for validating form inputs and error handling
in the BlazeDemo travel booking application.

Test Scenarios:
- Empty required fields validation
- Invalid email format handling
- Special characters in name fields
- Missing passenger information validation
"""

import pytest
from seleniumbase import BaseCase
from pages.blazedemo_pages.home_page import HomePage
from pages.blazedemo_pages.purchase_page import PurchasePage
from helpers.log_helpers import InlineLogger


class TestBlazeDemoFormValidation(BaseCase):
    """Test class for BlazeDemo form validation scenarios."""

    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()
        self.home_page = HomePage(self.driver)
        self.purchase_page = PurchasePage(self.driver)
        self.logger = InlineLogger()
        self.logger.log_step("🚀 Test setup completed")

    def test_empty_required_fields_validation(self):
        """
        Test validation of empty required fields in the booking form.
        
        Steps:
        1. Navigate to BlazeDemo home page
        2. Search for flights with valid criteria
        3. Select a flight
        4. Attempt to submit purchase form with empty required fields
        5. Verify appropriate error messages are displayed
        """
        self.logger.log_step("🧪 Starting empty required fields validation test")
        
        # Navigate to home page
        self.home_page.navigate_to_home()
        self.logger.log_step("✅ Navigated to BlazeDemo home page")
        
        # Search for flights with valid criteria
        self.home_page.search_flights("Paris", "London")
        self.logger.log_step("✅ Searched for flights: Paris to London")
        
        # Select first available flight
        self.home_page.select_first_flight()
        self.logger.log_step("✅ Selected first available flight")
        
        # Navigate to purchase page
        self.purchase_page.navigate_to_purchase()
        self.logger.log_step("✅ Navigated to purchase page")
        
        # Attempt to submit form with empty required fields
        self.purchase_page.submit_empty_form()
        self.logger.log_step("✅ Attempted to submit empty form")
        
        # Verify error messages are displayed
        error_present = self.purchase_page.verify_validation_errors()
        self.assertTrue(error_present, "❌ Validation errors should be displayed for empty required fields")
        self.logger.log_step("✅ Verified validation errors are displayed")
        
        self.logger.log_step("🎉 Empty required fields validation test completed successfully")

    def test_invalid_email_format_validation(self):
        """
        Test validation of invalid email formats in the booking form.
        
        Steps:
        1. Navigate to BlazeDemo home page
        2. Search for flights with valid criteria
        3. Select a flight
        4. Fill form with invalid email formats
        5. Verify appropriate error messages are displayed
        """
        self.logger.log_step("🧪 Starting invalid email format validation test")
        
        # Navigate to home page
        self.home_page.navigate_to_home()
        self.logger.log_step("✅ Navigated to BlazeDemo home page")
        
        # Search for flights with valid criteria
        self.home_page.search_flights("Boston", "New York")
        self.logger.log_step("✅ Searched for flights: Boston to New York")
        
        # Select first available flight
        self.home_page.select_first_flight()
        self.logger.log_step("✅ Selected first available flight")
        
        # Navigate to purchase page
        self.purchase_page.navigate_to_purchase()
        self.logger.log_step("✅ Navigated to purchase page")
        
        # Test various invalid email formats
        invalid_emails = [
            "invalid-email",
            "test@",
            "@domain.com",
            "test..test@domain.com",
            "test@domain",
            "test@.com"
        ]
        
        for email in invalid_emails:
            self.purchase_page.fill_form_with_invalid_email(email)
            self.logger.log_step(f"✅ Tested invalid email format: {email}")
            
            # Verify error message for invalid email
            error_present = self.purchase_page.verify_email_validation_error()
            self.assertTrue(error_present, f"❌ Email validation error should be displayed for: {email}")
            self.logger.log_step(f"✅ Verified email validation error for: {email}")
        
        self.logger.log_step("🎉 Invalid email format validation test completed successfully")

    def test_special_characters_in_name_fields(self):
        """
        Test handling of special characters in name fields.
        
        Steps:
        1. Navigate to BlazeDemo home page
        2. Search for flights with valid criteria
        3. Select a flight
        4. Fill name fields with special characters
        5. Verify proper handling or validation messages
        """
        self.logger.log_step("🧪 Starting special characters in name fields test")
        
        # Navigate to home page
        self.home_page.navigate_to_home()
        self.logger.log_step("✅ Navigated to BlazeDemo home page")
        
        # Search for flights with valid criteria
        self.home_page.search_flights("Berlin", "Rome")
        self.logger.log_step("✅ Searched for flights: Berlin to Rome")
        
        # Select first available flight
        self.home_page.select_first_flight()
        self.logger.log_step("✅ Selected first available flight")
        
        # Navigate to purchase page
        self.purchase_page.navigate_to_purchase()
        self.logger.log_step("✅ Navigated to purchase page")
        
        # Test special characters in name fields
        special_char_names = [
            "José María",
            "François",
            "Müller",
            "O'Connor",
            "Jean-Pierre",
            "José-Luis"
        ]
        
        for name in special_char_names:
            self.purchase_page.fill_form_with_special_char_name(name)
            self.logger.log_step(f"✅ Tested special character name: {name}")
            
            # Verify name is handled properly (either accepted or shows appropriate validation)
            name_handled = self.purchase_page.verify_name_field_handling(name)
            self.assertTrue(name_handled, f"❌ Name field should handle special characters properly: {name}")
            self.logger.log_step(f"✅ Verified name field handling for: {name}")
        
        self.logger.log_step("🎉 Special characters in name fields test completed successfully")

    def test_missing_passenger_information_validation(self):
        """
        Test validation when passenger information is missing.
        
        Steps:
        1. Navigate to BlazeDemo home page
        2. Search for flights with valid criteria
        3. Select a flight
        4. Fill form with missing passenger information
        5. Verify appropriate validation messages
        """
        self.logger.log_step("🧪 Starting missing passenger information validation test")
        
        # Navigate to home page
        self.home_page.navigate_to_home()
        self.logger.log_step("✅ Navigated to BlazeDemo home page")
        
        # Search for flights with valid criteria
        self.home_page.search_flights("Tokyo", "Seoul")
        self.logger.log_step("✅ Searched for flights: Tokyo to Seoul")
        
        # Select first available flight
        self.home_page.select_first_flight()
        self.logger.log_step("✅ Selected first available flight")
        
        # Navigate to purchase page
        self.purchase_page.navigate_to_purchase()
        self.logger.log_step("✅ Navigated to purchase page")
        
        # Fill form with missing passenger information
        self.purchase_page.fill_form_with_missing_passenger_info()
        self.logger.log_step("✅ Filled form with missing passenger information")
        
        # Attempt to submit form
        self.purchase_page.submit_form()
        self.logger.log_step("✅ Attempted to submit form")
        
        # Verify validation errors for missing passenger info
        validation_errors = self.purchase_page.verify_passenger_validation_errors()
        self.assertTrue(validation_errors, "❌ Validation errors should be displayed for missing passenger information")
        self.logger.log_step("✅ Verified passenger information validation errors")
        
        self.logger.log_step("🎉 Missing passenger information validation test completed successfully")

    def tearDown(self):
        """Clean up after each test."""
        self.logger.log_step("🧹 Test cleanup completed")
        super().tearDown()