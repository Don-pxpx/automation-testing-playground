import pytest
from seleniumbase import BaseCase
from pages.blazedemo_pages.purchase_page import PurchasePage


class BlazeDemoFormValidationTests(BaseCase):
    """Test suite for BlazeDemo form validation scenarios"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, sb):
        """Setup method to initialize page objects"""
        self.purchase_page = PurchasePage(sb)
        self.test = sb
    
    def test_empty_form_submission(self):
        """Test submitting form with no data filled"""
        self.purchase_page.open_purchase_page()
        
        # Submit empty form
        self.purchase_page.submit_empty_form()
        
        # Since BlazeDemo doesn't have validation, it will proceed to confirmation
        # We verify that the form accepts empty input and shows confirmation
        is_confirmation_shown = self.purchase_page.verify_validation_errors()
        assert is_confirmation_shown, "Empty form should be accepted by BlazeDemo (no validation)"
    
    def test_invalid_email_format(self):
        """Test form behavior with invalid email format"""
        self.purchase_page.open_purchase_page()
        
        # Fill form with invalid email format
        invalid_email = "invalid-email-format"
        self.purchase_page.fill_form_with_invalid_email(invalid_email)
        
        # Submit the form
        self.purchase_page.click_purchase_flight()
        
        # Since BlazeDemo doesn't have validation, it will accept invalid email
        is_email_accepted = self.purchase_page.verify_email_validation_error()
        assert is_email_accepted, "Invalid email format should be accepted by BlazeDemo (no validation)"
    
    def test_special_characters_in_name(self):
        """Test form behavior with special characters in name field"""
        self.purchase_page.open_purchase_page()
        
        # Fill form with special characters in name
        special_char_name = "Test@#$%^&*()User"
        self.purchase_page.fill_form_with_special_char_name(special_char_name)
        
        # Submit the form
        self.purchase_page.click_purchase_flight()
        
        # Since BlazeDemo doesn't have validation, it will accept special characters
        is_name_accepted = self.purchase_page.verify_name_field_handling(special_char_name)
        assert is_name_accepted, "Special characters in name should be accepted by BlazeDemo (no validation)"
    
    def test_missing_required_fields(self):
        """Test form behavior with missing required fields"""
        self.purchase_page.open_purchase_page()
        
        # Fill form with missing required fields
        self.purchase_page.fill_form_with_missing_fields()
        
        # Submit the form
        self.purchase_page.click_purchase_flight()
        
        # Since BlazeDemo doesn't have validation, it will accept incomplete form
        is_form_accepted = self.purchase_page.verify_required_field_validation()
        assert is_form_accepted, "Missing required fields should be accepted by BlazeDemo (no validation)"
    
    def test_form_accepts_any_input(self):
        """Test that BlazeDemo form accepts any input (demonstrates lack of validation)"""
        self.purchase_page.open_purchase_page()
        
        # Fill form with completely invalid data
        self.test.type(self.purchase_page.name_field, "!@#$%^&*()")
        self.test.type(self.purchase_page.address_field, "")
        self.test.type(self.purchase_page.city_field, "123456")
        self.test.type(self.purchase_page.state_field, "!@#")
        self.test.type(self.purchase_page.zip_code_field, "abc")
        self.test.select_option_by_text(self.purchase_page.card_type_dropdown, "American Express")
        self.test.type(self.purchase_page.credit_card_number_field, "invalid")
        self.test.type(self.purchase_page.credit_card_month_field, "99")
        self.test.type(self.purchase_page.credit_card_year_field, "1900")
        self.test.type(self.purchase_page.name_on_card_field, "")
        
        # Submit the form
        self.purchase_page.click_purchase_flight()
        
        # Verify that BlazeDemo accepts any input and proceeds to confirmation
        self.test.wait_for_element_visible("h1", timeout=10)
        confirmation_text = self.test.get_text("h1")
        assert "Thank you for your purchase today!" in confirmation_text, \
            "BlazeDemo should accept any input and proceed to confirmation (no validation)"
    
    def test_form_field_accessibility(self):
        """Test that all form fields are accessible and can be filled"""
        self.purchase_page.open_purchase_page()
        
        # Test that all fields are visible and accessible
        assert self.test.is_element_visible(self.purchase_page.name_field), "Name field should be visible"
        assert self.test.is_element_visible(self.purchase_page.address_field), "Address field should be visible"
        assert self.test.is_element_visible(self.purchase_page.city_field), "City field should be visible"
        assert self.test.is_element_visible(self.purchase_page.state_field), "State field should be visible"
        assert self.test.is_element_visible(self.purchase_page.zip_code_field), "Zip code field should be visible"
        assert self.test.is_element_visible(self.purchase_page.card_type_dropdown), "Card type dropdown should be visible"
        assert self.test.is_element_visible(self.purchase_page.credit_card_number_field), "Credit card number field should be visible"
        assert self.test.is_element_visible(self.purchase_page.credit_card_month_field), "Credit card month field should be visible"
        assert self.test.is_element_visible(self.purchase_page.credit_card_year_field), "Credit card year field should be visible"
        assert self.test.is_element_visible(self.purchase_page.name_on_card_field), "Name on card field should be visible"
        assert self.test.is_element_visible(self.purchase_page.purchase_flight_button), "Purchase flight button should be visible"
    
    def test_form_submission_button_functionality(self):
        """Test that the submit button works correctly"""
        self.purchase_page.open_purchase_page()
        
        # Fill form with valid data
        self.purchase_page.fill_user_details("John Doe", "123 Main St", "Anytown", "CA", "12345")
        self.purchase_page.fill_card_details("American Express", "1234567890123456", "12", "2025", "John Doe")
        
        # Submit the form
        self.purchase_page.click_purchase_flight()
        
        # Verify successful submission
        self.test.wait_for_element_visible("h1", timeout=10)
        confirmation_text = self.test.get_text("h1")
        assert "Thank you for your purchase today!" in confirmation_text, \
            "Form submission should be successful with valid data"