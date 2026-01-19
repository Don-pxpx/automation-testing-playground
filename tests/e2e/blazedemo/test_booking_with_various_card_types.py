import random
import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.pages.blazedemo_pages.home_page import HomePage
from automation_testing_playground.pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from automation_testing_playground.pages.blazedemo_pages.purchase_page import PurchasePage
from automation_testing_playground.pages.blazedemo_pages.confirmation_page import ConfirmationPage
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.blazedemo_models import (
    FlightSearch, PassengerInfo, PaymentDetails, BookingDetails
)

fake = Faker()

def test_booking_with_various_card_types(page: Page):
    """Test booking with different card types - INTENTIONALLY FAILS for one card type."""
    logger = InlineLogger()

    logger.step("Starting Test: Booking with Various Card Types")

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
    page.wait_for_selector("select[name='fromPort']", timeout=10000)
    home.select_flight_search(flight_search)
    home.click_find_flights()

    # Step 2: Wait for flights and choose random one
    logger.step("Waiting for flight listings and selecting a random flight")
    page.wait_for_selector("input[type='submit']", timeout=10000)
    assert flight.get_flight_count() > 0, "No flights found!"
    chosen_index = random.randint(0, flight.get_flight_count() - 1)
    logger.note(f"Chosen Flight Index: {chosen_index}")
    flight.select_flight_by_index(chosen_index)

    # Step 3: Fill in purchase details with random card types
    logger.step("Filling purchase details with random card information")
    card_types = ["Visa", "American Express", "Diner's Club"]
    card_type = random.choice(card_types)
    
    # INTENTIONAL FAILURE: Simulate a validation issue with Diner's Club
    # In real scenarios, some card types might have different validation rules
    if card_type == "Diner's Club":
        # Use an invalid card number length for Diner's Club (should be 14 digits, using 16)
        card_number = ''.join(random.choices("1234567890", k=16))  # Wrong length for Diner's Club
        logger.warning(f"Using potentially invalid card number length for {card_type}")
    else:
        card_number = ''.join(random.choices("1234567890", k=16))

    name = fake.name()
    address = f"{random.randint(100, 999)} {random.choice(['Elm', 'Maple', 'Oak'])} St"
    city = random.choice(["NY", "LA", "Chicago"])
    state = random.choice(["NY", "CA", "IL"])
    zip_code = str(random.randint(10000, 99999))
    exp_month = str(random.randint(1, 12)).zfill(2)
    exp_year = str(random.randint(2025, 2030))

    logger.note(f"Card Type: {card_type}")
    logger.note(f"Card Number (Masked): **** **** **** {card_number[-4:]}")

    # Create Pydantic models
    passenger_info = PassengerInfo(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code
    )

    try:
        payment_details = PaymentDetails(
            card_type=card_type,
            card_number=card_number,
            expiry_month=exp_month,
            expiry_year=exp_year,
            name_on_card=name
        )
    except Exception as e:
        # INTENTIONAL FAILURE: Card validation fails for Diner's Club
        logger.error(f"Payment validation failed for {card_type}: {str(e)}")
        raise AssertionError(f"Card validation failed - {card_type} requires 14 digits but got {len(card_number)} digits")

    booking_details = BookingDetails(
        flight_search=flight_search,
        passenger_info=passenger_info,
        payment_details=payment_details,
        remember_me=False
    )

    purchase.fill_booking_details(booking_details)
    purchase.submit_purchase()

    # Verify confirmation
    assert confirm.is_confirmation_successful(), f"Booking confirmation failed for {card_type}!"
    logger.success(f"Booking completed successfully with {card_type}")
