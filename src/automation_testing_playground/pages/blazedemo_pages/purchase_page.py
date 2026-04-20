from playwright.sync_api import Page, expect

from automation_testing_playground.config.blazedemo_config import BlazeDemoData
from automation_testing_playground.config.settings import TEST_TARGETS_CONFIG
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.blazedemo_models import (
    BookingDetails,
    PassengerInfo,
    PaymentDetails,
)


class PurchasePage:
    """Purchase / payment façade — UI adaptation stays here (POM); tests orchestrate only."""

    _CONFIRMATION_HEADING = "h1"
    _PRICE_LINE = "p:has-text('Price')"

    def __init__(self, page: Page):
        self.page = page
        self.logger = InlineLogger()

        self._name_field = "input#inputName"
        self._address_field = "input#address"
        self._city_field = "input#city"
        self._state_field = "input#state"
        self._zip_code_field = "input#zipCode"
        self._card_type_dropdown = "select#cardType"
        self._credit_card_number_field = "input#creditCardNumber"
        self._credit_card_month_field = "input#creditCardMonth"
        self._credit_card_year_field = "input#creditCardYear"
        self._name_on_card_field = "input#nameOnCard"
        self._remember_me_checkbox = "input#rememberMe"
        self._purchase_flight_button = "input[type='submit']"

    def open_purchase_page(self) -> None:
        base = TEST_TARGETS_CONFIG.DEMO_APPS["blazedemo"].rstrip("/")
        self.page.goto(f"{base}/purchase.php")
        self.page.wait_for_selector(self._name_field, timeout=15000)

    def fill_user_details(self, name: str, address: str, city: str, state: str, zip_code: str) -> None:
        self.page.wait_for_selector(self._name_field, timeout=15000)
        self.page.fill(self._name_field, name)
        self.page.fill(self._address_field, address)
        self.page.fill(self._city_field, city)
        self.page.fill(self._state_field, state)
        self.page.fill(self._zip_code_field, zip_code)

    def fill_passenger_info(self, passenger_info: PassengerInfo) -> None:
        self.fill_user_details(
            passenger_info.name,
            passenger_info.address,
            passenger_info.city,
            passenger_info.state,
            passenger_info.zip_code,
        )

    def fill_card_details(self, card_type: str, card_number: str, month: str, year: str, name_on_card: str) -> None:
        self.page.select_option(self._card_type_dropdown, label=card_type)
        self.page.fill(self._credit_card_number_field, card_number)
        self.page.fill(self._credit_card_month_field, month)
        self.page.fill(self._credit_card_year_field, year)
        self.page.fill(self._name_on_card_field, name_on_card)

    def fill_payment_details(self, payment_details: PaymentDetails) -> None:
        self.fill_card_details(
            payment_details.card_type,
            payment_details.card_number,
            payment_details.expiry_month,
            payment_details.expiry_year,
            payment_details.name_on_card,
        )

    def fill_booking_details(self, booking_details: BookingDetails) -> None:
        booking_details.validate()
        self.fill_passenger_info(booking_details.passenger_info)
        self.fill_payment_details(booking_details.payment_details)
        if booking_details.remember_me:
            self.toggle_remember_me()

    def click_purchase_flight(self) -> None:
        self.page.click(self._purchase_flight_button)

    def submit_purchase(self) -> None:
        self.click_purchase_flight()

    def toggle_remember_me(self) -> None:
        self.page.click(self._remember_me_checkbox)

    def set_card_expiry(self, month: str, year: str) -> None:
        self.page.fill(self._credit_card_month_field, month)
        self.page.fill(self._credit_card_year_field, year)

    def select_card_type(self, card_type: str) -> None:
        self.page.select_option(self._card_type_dropdown, label=card_type)

    def set_card_name(self, name: str) -> None:
        self.page.fill(self._name_on_card_field, name)

    def fill_form_with_invalid_email(self, email: str) -> None:
        self.page.fill(self._name_field, email)
        self.page.fill(self._address_field, "123 Test St")
        self.page.fill(self._city_field, "Test City")
        self.page.fill(self._state_field, "TS")
        self.page.fill(self._zip_code_field, "12345")
        self.page.select_option(self._card_type_dropdown, label=BlazeDemoData.DEMO_CARD_TYPE)
        self.page.fill(self._credit_card_number_field, BlazeDemoData.DEMO_CARD_NUMBER)
        self.page.fill(self._credit_card_month_field, BlazeDemoData.DEMO_EXPIRY_MONTH)
        self.page.fill(self._credit_card_year_field, BlazeDemoData.DEMO_EXPIRY_YEAR)
        self.page.fill(self._name_on_card_field, BlazeDemoData.DEMO_NAME_ON_CARD)

    def verify_email_validation_error(self) -> bool:
        self.page.wait_for_selector(self._CONFIRMATION_HEADING, timeout=10000)
        confirmation_text = self.page.locator(self._CONFIRMATION_HEADING).text_content() or ""
        return "Thank you for your purchase today!" in confirmation_text

    def fill_form_with_special_char_name(self, name: str) -> None:
        self.page.fill(self._name_field, name)
        self.page.fill(self._address_field, "123 Test St")
        self.page.fill(self._city_field, "Test City")
        self.page.fill(self._state_field, "TS")
        self.page.fill(self._zip_code_field, "12345")
        self.page.select_option(self._card_type_dropdown, label=BlazeDemoData.DEMO_CARD_TYPE)
        self.page.fill(self._credit_card_number_field, BlazeDemoData.DEMO_CARD_NUMBER)
        self.page.fill(self._credit_card_month_field, BlazeDemoData.DEMO_EXPIRY_MONTH)
        self.page.fill(self._credit_card_year_field, BlazeDemoData.DEMO_EXPIRY_YEAR)
        self.page.fill(self._name_on_card_field, BlazeDemoData.DEMO_NAME_ON_CARD)

    def verify_name_field_handling(self, _name: str) -> bool:
        self.page.wait_for_selector(self._CONFIRMATION_HEADING, timeout=10000)
        confirmation_text = self.page.locator(self._CONFIRMATION_HEADING).text_content() or ""
        return "Thank you for your purchase today!" in confirmation_text

    def fill_form_with_missing_fields(self) -> None:
        self.page.fill(self._name_field, "Test User")
        self.page.fill(self._address_field, "123 Test St")
        self.page.select_option(self._card_type_dropdown, label=BlazeDemoData.DEMO_CARD_TYPE)
        self.page.fill(self._credit_card_number_field, BlazeDemoData.DEMO_CARD_NUMBER)
        self.page.fill(self._credit_card_month_field, BlazeDemoData.DEMO_EXPIRY_MONTH)
        self.page.fill(self._credit_card_year_field, BlazeDemoData.DEMO_EXPIRY_YEAR)
        self.page.fill(self._name_on_card_field, BlazeDemoData.DEMO_NAME_ON_CARD)

    def verify_required_field_validation(self) -> bool:
        self.page.wait_for_selector(self._CONFIRMATION_HEADING, timeout=10000)
        confirmation_text = self.page.locator(self._CONFIRMATION_HEADING).text_content() or ""
        return "Thank you for your purchase today!" in confirmation_text

    def submit_empty_form(self) -> None:
        self.page.click(self._purchase_flight_button)

    def verify_validation_errors(self) -> bool:
        self.page.wait_for_selector(self._CONFIRMATION_HEADING, timeout=10000)
        confirmation_text = self.page.locator(self._CONFIRMATION_HEADING).text_content() or ""
        return "Thank you for your purchase today!" in confirmation_text

    def is_on_purchase_page(self) -> bool:
        return self.page.locator(self._name_field).is_visible()

    def get_page_title(self) -> str:
        return self.page.title()

    def get_confirmation_heading_text(self) -> str:
        """Text of the post-submit confirmation heading (BlazeDemo uses h1)."""
        self.page.wait_for_selector(self._CONFIRMATION_HEADING, timeout=10000)
        return self.page.locator(self._CONFIRMATION_HEADING).text_content() or ""

    def fill_and_submit_extreme_invalid_values(self) -> None:
        """Deliberately invalid / edge values for negative-path demos (all via façade)."""
        self.page.fill(self._name_field, "!@#$%^&*()")
        self.page.fill(self._address_field, "")
        self.page.fill(self._city_field, "123456")
        self.page.fill(self._state_field, "!@#")
        self.page.fill(self._zip_code_field, "abc")
        self.page.select_option(self._card_type_dropdown, label="American Express")
        self.page.fill(self._credit_card_number_field, "invalid")
        self.page.fill(self._credit_card_month_field, "99")
        self.page.fill(self._credit_card_year_field, "1900")
        self.page.fill(self._name_on_card_field, "")
        self.click_purchase_flight()

    def assert_purchase_form_fields_visible(self) -> None:
        """Assert all purchase controls are visible — locators stay inside the façade."""
        expect(self.page.locator(self._name_field)).to_be_visible()
        expect(self.page.locator(self._address_field)).to_be_visible()
        expect(self.page.locator(self._city_field)).to_be_visible()
        expect(self.page.locator(self._state_field)).to_be_visible()
        expect(self.page.locator(self._zip_code_field)).to_be_visible()
        expect(self.page.locator(self._card_type_dropdown)).to_be_visible()
        expect(self.page.locator(self._credit_card_number_field)).to_be_visible()
        expect(self.page.locator(self._credit_card_month_field)).to_be_visible()
        expect(self.page.locator(self._credit_card_year_field)).to_be_visible()
        expect(self.page.locator(self._name_on_card_field)).to_be_visible()
        expect(self.page.locator(self._purchase_flight_button)).to_be_visible()

    def get_fare_line_text_near_price_label(self) -> str:
        """Raw text from the first 'Price' line on the purchase page (for booking vs confirmation checks)."""
        el = self.page.locator(self._PRICE_LINE).first
        if el.is_visible():
            return el.text_content() or ""
        return ""
