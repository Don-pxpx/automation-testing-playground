import pytest
from playwright.sync_api import Page

from automation_testing_playground.config.blazedemo_config import BlazeDemoData
from automation_testing_playground.pages.blazedemo_pages.purchase_page import PurchasePage


class BlazeDemoFormValidationTests:
    """Test suite for BlazeDemo form validation scenarios"""


def test_empty_form_submission(page: Page):
    """BZD-FORM-001: Empty purchase form submission behaviour (functional correctness)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    purchase_page.submit_empty_form()

    is_confirmation_shown = purchase_page.verify_validation_errors()
    assert is_confirmation_shown, "Empty form should be accepted by BlazeDemo (no validation)"


def test_invalid_email_format(page: Page):
    """BZD-FORM-002: Invalid email format handling (functional correctness)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    invalid_email = "invalid-email-format"
    purchase_page.fill_form_with_invalid_email(invalid_email)

    purchase_page.click_purchase_flight()

    is_email_accepted = purchase_page.verify_email_validation_error()
    assert is_email_accepted, "Invalid email format should be accepted by BlazeDemo (no validation)"


def test_special_characters_in_name(page: Page):
    """BZD-FORM-003: Special characters in passenger name (functional correctness)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    special_char_name = "Test@#$%^&*()User"
    purchase_page.fill_form_with_special_char_name(special_char_name)

    purchase_page.click_purchase_flight()

    is_name_accepted = purchase_page.verify_name_field_handling(special_char_name)
    assert is_name_accepted, "Special characters in name should be accepted by BlazeDemo"


def test_missing_required_fields(page: Page):
    """BZD-FORM-004: Partially filled purchase form (functional correctness)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    purchase_page.fill_form_with_missing_fields()

    purchase_page.click_purchase_flight()

    is_form_accepted = purchase_page.verify_required_field_validation()
    assert is_form_accepted, "Missing required fields should be accepted by BlazeDemo (no validation)"


@pytest.mark.xfail(
    reason="BZD-FORM-005: BlazeDemo accepts extreme invalid values (demo site validation gap)",
    strict=False,
)
def test_extreme_input_values(page: Page):
    """BZD-FORM-005: Extreme invalid inputs (known BlazeDemo validation gap)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    purchase_page.fill_and_submit_extreme_invalid_values()

    confirmation_text = purchase_page.get_confirmation_heading_text()

    assert "Thank you" not in confirmation_text, (
        "Form should reject extreme invalid values but BlazeDemo accepts them (validation bug)"
    )


def test_form_field_visibility(page: Page):
    """BZD-FORM-006: Purchase form fields are visible (functional completeness)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    purchase_page.assert_purchase_form_fields_visible()


def test_valid_form_submission(page: Page):
    """BZD-FORM-007: Valid purchase shows thank-you confirmation (functional correctness)."""
    purchase_page = PurchasePage(page)
    purchase_page.open_purchase_page()

    purchase_page.fill_user_details("John Doe", "123 Main St", "Anytown", "CA", "12345")
    purchase_page.fill_card_details(
        BlazeDemoData.DEMO_CARD_TYPE,
        BlazeDemoData.DEMO_CARD_NUMBER,
        BlazeDemoData.DEMO_EXPIRY_MONTH,
        BlazeDemoData.DEMO_EXPIRY_YEAR,
        BlazeDemoData.DEMO_NAME_ON_CARD,
    )

    purchase_page.click_purchase_flight()

    confirmation_text = purchase_page.get_confirmation_heading_text()
    assert "Thank you for your purchase today!" in confirmation_text, (
        "Valid form submission should show confirmation"
    )
