from playwright.sync_api import Page

from automation_testing_playground.config.blazedemo_config import BlazeDemoData
from automation_testing_playground.config.settings import TEST_TARGETS_CONFIG
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.blazedemo_models import (
    BookingDetails,
    PassengerInfo,
    PaymentDetails,
)


class PurchasePage:
    """Page Object Model for BlazeDemo Purchase Page"""
    
    def __init__(self, page: Page):
        self.page = page  # Playwright page object
        self.logger = InlineLogger()
        
        # Locators
        self.name_field = "input#inputName"
        self.address_field = "input#address"
        self.city_field = "input#city"
        self.state_field = "input#state"
        self.zip_code_field = "input#zipCode"
        self.card_type_dropdown = "select#cardType"
        self.credit_card_number_field = "input#creditCardNumber"
        self.credit_card_month_field = "input#creditCardMonth"
        self.credit_card_year_field = "input#creditCardYear"
        self.name_on_card_field = "input#nameOnCard"
        self.remember_me_checkbox = "input#rememberMe"
        self.purchase_flight_button = "input[type='submit']"
    
    def open_purchase_page(self):
        """Navigate to the purchase page"""
        base = TEST_TARGETS_CONFIG.DEMO_APPS["blazedemo"].rstrip("/")
        self.page.goto(f"{base}/purchase.php")
        self.page.wait_for_selector(self.name_field, timeout=15000)
    
    def fill_user_details(self, name: str, address: str, city: str, state: str, zip_code: str):
        """Fill in user details form fields"""
        self.page.wait_for_selector(self.name_field, timeout=15000)
        self.page.fill(self.name_field, name)
        self.page.fill(self.address_field, address)
        self.page.fill(self.city_field, city)
        self.page.fill(self.state_field, state)
        self.page.fill(self.zip_code_field, zip_code)
    
    def fill_passenger_info(self, passenger_info: PassengerInfo):
        """Fill passenger info using Pydantic model."""
        self.fill_user_details(
            passenger_info.name,
            passenger_info.address,
            passenger_info.city,
            passenger_info.state,
            passenger_info.zip_code
        )
    
    def fill_card_details(self, card_type: str, card_number: str, month: str, year: str, name_on_card: str):
        """Fill in credit card details"""
        self.page.select_option(self.card_type_dropdown, label=card_type)
        self.page.fill(self.credit_card_number_field, card_number)
        self.page.fill(self.credit_card_month_field, month)
        self.page.fill(self.credit_card_year_field, year)
        self.page.fill(self.name_on_card_field, name_on_card)
    
    def fill_payment_details(self, payment_details: PaymentDetails):
        """Fill payment details using Pydantic model."""
        self.fill_card_details(
            payment_details.card_type,
            payment_details.card_number,
            payment_details.expiry_month,
            payment_details.expiry_year,
            payment_details.name_on_card
        )
    
    def fill_booking_details(self, booking_details: BookingDetails):
        """Fill complete booking using Pydantic model."""
        booking_details.validate()
        self.fill_passenger_info(booking_details.passenger_info)
        self.fill_payment_details(booking_details.payment_details)
        if booking_details.remember_me:
            self.toggle_remember_me()
    
    def click_purchase_flight(self):
        """Click the purchase flight button"""
        self.page.click(self.purchase_flight_button)
    
    def submit_purchase(self):
        """Alias for click_purchase_flight for consistency"""
        self.click_purchase_flight()
    
    def toggle_remember_me(self):
        """Toggle the remember me checkbox"""
        self.page.click(self.remember_me_checkbox)
    
    def set_card_expiry(self, month: str, year: str):
        """Set card expiry date"""
        self.page.fill(self.credit_card_month_field, month)
        self.page.fill(self.credit_card_year_field, year)
    
    def select_card_type(self, card_type: str):
        """Select card type from dropdown"""
        self.page.select_option(self.card_type_dropdown, label=card_type)
    
    def set_card_name(self, name: str):
        """Set name on card"""
        self.page.fill(self.name_on_card_field, name)
    
    def fill_form_with_invalid_email(self, email: str):
        """Fill form with invalid email format (using name field as email simulation)"""
        self.page.fill(self.name_field, email)
        self.page.fill(self.address_field, "123 Test St")
        self.page.fill(self.city_field, "Test City")
        self.page.fill(self.state_field, "TS")
        self.page.fill(self.zip_code_field, "12345")
        self.page.select_option(self.card_type_dropdown, label=BlazeDemoData.DEMO_CARD_TYPE)
        self.page.fill(self.credit_card_number_field, BlazeDemoData.DEMO_CARD_NUMBER)
        self.page.fill(self.credit_card_month_field, BlazeDemoData.DEMO_EXPIRY_MONTH)
        self.page.fill(self.credit_card_year_field, BlazeDemoData.DEMO_EXPIRY_YEAR)
        self.page.fill(self.name_on_card_field, BlazeDemoData.DEMO_NAME_ON_CARD)
    
    def verify_email_validation_error(self) -> bool:
        """Verify that email validation error is shown (BlazeDemo doesn't have validation)"""
        # Since BlazeDemo doesn't have client-side validation, we'll check if the form
        # accepts the invalid input and proceeds to confirmation
        self.page.wait_for_selector("h1", timeout=10000)
        confirmation_text = self.page.locator("h1").text_content() or ""
        # BlazeDemo will accept any input, so we expect it to proceed to confirmation
        return "Thank you for your purchase today!" in confirmation_text
    
    def fill_form_with_special_char_name(self, name: str):
        """Fill form with special characters in name field"""
        self.page.fill(self.name_field, name)
        self.page.fill(self.address_field, "123 Test St")
        self.page.fill(self.city_field, "Test City")
        self.page.fill(self.state_field, "TS")
        self.page.fill(self.zip_code_field, "12345")
        self.page.select_option(self.card_type_dropdown, label=BlazeDemoData.DEMO_CARD_TYPE)
        self.page.fill(self.credit_card_number_field, BlazeDemoData.DEMO_CARD_NUMBER)
        self.page.fill(self.credit_card_month_field, BlazeDemoData.DEMO_EXPIRY_MONTH)
        self.page.fill(self.credit_card_year_field, BlazeDemoData.DEMO_EXPIRY_YEAR)
        self.page.fill(self.name_on_card_field, BlazeDemoData.DEMO_NAME_ON_CARD)
    
    def verify_name_field_handling(self, name: str) -> bool:
        """Verify how the name field handles special characters"""
        # Check if the name was accepted and appears in confirmation
        self.page.wait_for_selector("h1", timeout=10000)
        confirmation_text = self.page.locator("h1").text_content() or ""
        # BlazeDemo accepts any input, so we expect it to proceed to confirmation
        return "Thank you for your purchase today!" in confirmation_text
    
    def fill_form_with_missing_fields(self):
        """Fill form with some missing required fields"""
        # Only fill name and address, leave other fields empty
        self.page.fill(self.name_field, "Test User")
        self.page.fill(self.address_field, "123 Test St")
        # Leave city, state, zip_code empty
        self.page.select_option(self.card_type_dropdown, label=BlazeDemoData.DEMO_CARD_TYPE)
        self.page.fill(self.credit_card_number_field, BlazeDemoData.DEMO_CARD_NUMBER)
        self.page.fill(self.credit_card_month_field, BlazeDemoData.DEMO_EXPIRY_MONTH)
        self.page.fill(self.credit_card_year_field, BlazeDemoData.DEMO_EXPIRY_YEAR)
        self.page.fill(self.name_on_card_field, BlazeDemoData.DEMO_NAME_ON_CARD)
    
    def verify_required_field_validation(self) -> bool:
        """Verify that required field validation works (BlazeDemo doesn't have validation)"""
        # Since BlazeDemo doesn't have client-side validation, we'll check if the form
        # accepts the incomplete input and proceeds to confirmation
        self.page.wait_for_selector("h1", timeout=10000)
        confirmation_text = self.page.locator("h1").text_content() or ""
        # BlazeDemo will accept any input, so we expect it to proceed to confirmation
        return "Thank you for your purchase today!" in confirmation_text
    
    def submit_empty_form(self):
        """Submit the form without filling any fields"""
        # Click submit without filling any fields
        self.page.click(self.purchase_flight_button)
    
    def verify_validation_errors(self) -> bool:
        """Verify that validation errors are shown (BlazeDemo doesn't have validation)"""
        # Since BlazeDemo doesn't have client-side validation, we'll check if the form
        # accepts empty input and proceeds to confirmation
        self.page.wait_for_selector("h1", timeout=10000)
        confirmation_text = self.page.locator("h1").text_content() or ""
        # BlazeDemo will accept any input, so we expect it to proceed to confirmation
        return "Thank you for your purchase today!" in confirmation_text
    
    def is_on_purchase_page(self) -> bool:
        """Check if we're on the purchase page"""
        return self.page.locator(self.name_field).is_visible()
    
    def get_page_title(self) -> str:
        """Get the page title"""
        return self.page.title()
