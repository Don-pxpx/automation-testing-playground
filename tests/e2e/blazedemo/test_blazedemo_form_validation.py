import pytest
from playwright.sync_api import Page, expect
from automation_testing_playground.pages.blazedemo_pages.purchase_page import PurchasePage

class BlazeDemoFormValidationTests:
    """Test suite for BlazeDemo form validation scenarios"""

def test_empty_form_submission(page: Page):
    """Test submitting form with no data filled."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    # Submit empty form
    purchase_page.submit_empty_form()
    
    # Since BlazeDemo doesn't have validation, it will proceed to confirmation
    # We verify that the form accepts empty input and shows confirmation
    is_confirmation_shown = purchase_page.verify_validation_errors()
    assert is_confirmation_shown, "Empty form should be accepted by BlazeDemo (no validation)"

def test_invalid_email_format(page: Page):
    """Test form behavior with invalid email format."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    # Fill form with invalid email format
    invalid_email = "invalid-email-format"
    purchase_page.fill_form_with_invalid_email(invalid_email)
    
    # Submit the form
    purchase_page.click_purchase_flight()
    
    # Since BlazeDemo doesn't have validation, it will accept invalid email
    is_email_accepted = purchase_page.verify_email_validation_error()
    assert is_email_accepted, "Invalid email format should be accepted by BlazeDemo (no validation)"

def test_special_characters_in_name(page: Page):
    """Test form behavior with special characters in name field."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    # Fill form with special characters in name
    special_char_name = "Test@#$%^&*()User"
    purchase_page.fill_form_with_special_char_name(special_char_name)
    
    # Submit the form
    purchase_page.click_purchase_flight()
    
    # Verify special characters are handled
    is_name_accepted = purchase_page.verify_name_field_handling(special_char_name)
    assert is_name_accepted, "Special characters in name should be accepted by BlazeDemo"

def test_missing_required_fields(page: Page):
    """Test form behavior with missing required fields."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    # Fill form with some missing required fields
    purchase_page.fill_form_with_missing_fields()
    
    # Submit the form
    purchase_page.click_purchase_flight()
    
    # Since BlazeDemo doesn't have validation, it will accept incomplete input
    is_form_accepted = purchase_page.verify_required_field_validation()
    assert is_form_accepted, "Missing required fields should be accepted by BlazeDemo (no validation)"

def test_extreme_input_values(page: Page):
    """Test form behavior with extreme input values - INTENTIONALLY FAILS."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    # Fill form with extreme/invalid values
    # INTENTIONAL FAILURE: Some fields might not accept extreme values
    page.fill(purchase_page.name_field, "!@#$%^&*()")
    page.fill(purchase_page.address_field, "")
    page.fill(purchase_page.city_field, "123456")
    page.fill(purchase_page.state_field, "!@#")
    page.fill(purchase_page.zip_code_field, "abc")
    page.select_option(purchase_page.card_type_dropdown, label="American Express")
    page.fill(purchase_page.credit_card_number_field, "invalid")
    page.fill(purchase_page.credit_card_month_field, "99")
    page.fill(purchase_page.credit_card_year_field, "1900")
    page.fill(purchase_page.name_on_card_field, "")
    
    purchase_page.click_purchase_flight()
    
    # INTENTIONAL FAILURE: This should fail validation but BlazeDemo accepts it
    # We'll assert that it should fail, but it won't - simulating a real bug
    page.wait_for_selector("h1", timeout=10000)
    confirmation_text = page.locator("h1").text_content() or ""
    
    # This assertion will fail because BlazeDemo accepts invalid data
    # This simulates a real-world scenario where validation should catch this but doesn't
    assert "Thank you" not in confirmation_text, "Form should reject extreme invalid values but BlazeDemo accepts them (validation bug)"
    
    purchase_page.open_purchase_page()

def test_form_field_visibility(page: Page):
    """Test that all form fields are visible and accessible."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    assert page.locator(purchase_page.name_field).is_visible(), "Name field should be visible"
    assert page.locator(purchase_page.address_field).is_visible(), "Address field should be visible"
    assert page.locator(purchase_page.city_field).is_visible(), "City field should be visible"
    assert page.locator(purchase_page.state_field).is_visible(), "State field should be visible"
    assert page.locator(purchase_page.zip_code_field).is_visible(), "Zip code field should be visible"
    assert page.locator(purchase_page.card_type_dropdown).is_visible(), "Card type dropdown should be visible"
    assert page.locator(purchase_page.credit_card_number_field).is_visible(), "Credit card number field should be visible"
    assert page.locator(purchase_page.credit_card_month_field).is_visible(), "Credit card month field should be visible"
    assert page.locator(purchase_page.credit_card_year_field).is_visible(), "Credit card year field should be visible"
    assert page.locator(purchase_page.name_on_card_field).is_visible(), "Name on card field should be visible"
    assert page.locator(purchase_page.purchase_flight_button).is_visible(), "Purchase flight button should be visible"

def test_valid_form_submission(page: Page):
    """Test successful form submission with valid data."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()
    
    # Fill form with valid data
    purchase_page.fill_user_details("John Doe", "123 Main St", "Anytown", "CA", "12345")
    purchase_page.fill_card_details("American Express", "1234567890123456", "12", "2025", "John Doe")
    
    # Submit the form
    purchase_page.click_purchase_flight()
    
    # Verify confirmation
    page.wait_for_selector("h1", timeout=10000)
    confirmation_text = page.locator("h1").text_content() or ""
    assert "Thank you for your purchase today!" in confirmation_text, "Valid form submission should show confirmation"
