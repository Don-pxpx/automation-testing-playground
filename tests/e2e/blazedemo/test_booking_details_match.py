import random
import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.blazedemo_pages.home_page import HomePage
from automation_testing_playground.pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from automation_testing_playground.pages.blazedemo_pages.purchase_page import PurchasePage
from automation_testing_playground.pages.blazedemo_pages.confirmation_page import ConfirmationPage
from automation_testing_playground.models.blazedemo_models import (
    FlightSearch, PassengerInfo, PaymentDetails, BookingDetails
)

fake = Faker()

def test_booking_details_match(page: Page):
    """Test that booking details match between purchase and confirmation - INTENTIONALLY FAILS on price comparison."""
    logger = InlineLogger()
    logger.step("Starting Test: Booking Details Match")

    home = HomePage(page)
    flight = FlightSelectionPage(page)
    purchase = PurchasePage(page)
    confirm = ConfirmationPage(page)

    # Step 1: Navigate to homepage and select cities randomly
    logger.step("Navigating to BlazeDemo homepage and selecting cities")
    departure_cities = ["Boston", "Philadelphia", "Portland", "San Diego", "Mexico City", "São Paolo"]
    destination_cities = ["New York", "Berlin", "Rome", "London"]

    departure_city = random.choice(departure_cities)
    destination_city = random.choice([city for city in destination_cities if city != departure_city])

    logger.note(f"Selected Departure City: {departure_city}")
    logger.note(f"Selected Destination City: {destination_city}")

    flight_search = FlightSearch(
        departure_city=departure_city,
        destination_city=destination_city
    )

    home.open_homepage()
    home.select_flight_search(flight_search)
    home.click_find_flights()

    # Step 2: Choose a random flight
    logger.step("Waiting for flight listings and selecting a random flight")
    page.wait_for_selector("input[type='submit']", timeout=10000)
    flight_count = flight.get_flight_count()
    assert flight_count > 0, "No flights available!"
    chosen_index = random.randint(0, flight_count - 1)
    logger.note(f"Chosen Flight Index: {chosen_index}")
    flight.select_flight_by_index(chosen_index)

    # Step 3: Fill in user and payment details
    logger.step("Filling purchase details with random user and card information")
    name = fake.name()
    address = f"{random.randint(100, 999)} {random.choice(['Elm', 'Maple', 'Oak'])} St"
    city = random.choice(["NY", "LA", "Chicago"])
    state = random.choice(["NY", "CA", "IL"])
    zip_code = str(random.randint(10000, 99999))
    card_number = ''.join(random.choices("1234567890", k=16))
    card_type = "Visa"
    exp_month = str(random.randint(1, 12)).zfill(2)
    exp_year = str(random.randint(2025, 2030))

    # Get price from purchase page before submitting
    # INTENTIONAL FAILURE: Price might not be captured correctly or might change
    try:
        price_element = page.locator("p:has-text('Price')").first
        if price_element.is_visible():
            price_text = price_element.text_content() or ""
            expected_price = price_text.split("$")[-1].strip() if "$" in price_text else "Unknown"
            logger.note(f"Expected price from purchase page: ${expected_price}")
        else:
            expected_price = "Unknown"
            logger.warning("Could not find price element on purchase page")
    except Exception as e:
        expected_price = "Unknown"
        logger.warning(f"Error extracting price: {str(e)}")

    passenger_info = PassengerInfo(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code
    )

    payment_details = PaymentDetails(
        card_type=card_type,
        card_number=card_number,
        expiry_month=exp_month,
        expiry_year=exp_year,
        name_on_card=name
    )

    booking_details = BookingDetails(
        flight_search=flight_search,
        passenger_info=passenger_info,
        payment_details=payment_details,
        remember_me=False
    )

    purchase.fill_booking_details(booking_details)
    purchase.submit_purchase()

    # Step 4: Verify confirmation and compare details
    logger.step("Validating Booking Confirmation and Comparing Details")
    assert confirm.is_confirmation_successful(), "Booking confirmation failed!"
    
    confirmation_details = confirm.get_booking_details()
    logger.note(f"Confirmation details: {confirmation_details}")

    # INTENTIONAL FAILURE: Price comparison might fail due to formatting differences
    if expected_price != "Unknown" and "Total Cost" in confirmation_details:
        actual_price = confirmation_details.get("Total Cost", "").replace("$", "").replace(",", "").strip()
        expected_price_clean = expected_price.replace("$", "").replace(",", "").strip()
        
        if actual_price != expected_price_clean:
            logger.error(f"Price mismatch: Expected ${expected_price_clean}, Got ${actual_price}")
            # This simulates a real-world issue where prices might differ due to taxes, fees, or formatting
            raise AssertionError(f"Price mismatch detected - Expected ${expected_price_clean}, but confirmation shows ${actual_price}. This could indicate a calculation or display issue.")
        else:
            logger.success(f"Price matches: ${actual_price}")
    else:
        logger.warning("Could not compare prices - price information not available")

    logger.success("Booking details verification completed")
