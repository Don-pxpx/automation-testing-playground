import random
import pytest
from playwright.sync_api import Page, expect
from faker import Faker

from automation_testing_playground.pages.blazedemo_pages.home_page import HomePage
from automation_testing_playground.pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from automation_testing_playground.pages.blazedemo_pages.purchase_page import PurchasePage
from automation_testing_playground.pages.blazedemo_pages.confirmation_page import ConfirmationPage
from automation_testing_playground.config import credentials
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.models.blazedemo_models import (
    FlightSearch, BookingDetails, PassengerInfo, PaymentDetails
)

fake = Faker()

def test_complete_booking_flow(page: Page):
    """Test complete booking flow with Pydantic models."""
    logger = InlineLogger()
    logger.step("Starting Test: Complete Booking Flow")

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
    flight_search.validate_different_cities()

    home.open_homepage()
    page.wait_for_selector("select[name='fromPort']", timeout=10000)
    home.select_flight_search(flight_search)
    home.click_find_flights()

    # Step 2: Assert and choose random flight
    logger.step("Waiting for available flights and selecting a random flight")
    page.wait_for_selector("input[type='submit']", timeout=10000)
    flight_count = flight.get_flight_count()
    assert flight_count > 0, "No flights found!"
    logger.note(f"Total Flights Found: {flight_count}")
    airline_names = flight.get_airline_names()
    if airline_names:
        logger.note(f"First Airline Listed: {airline_names[0]}")

    chosen_index = random.randint(0, flight_count - 1)
    logger.note(f"Chosen Flight Index: {chosen_index}")
    flight.select_flight_by_index(chosen_index)

    # Step 3: Generate random but valid user and card details using Pydantic
    logger.step("Generating Random User & Card Details")
    name = f"{random.choice(['John', 'Jane', 'Chris', 'Alex'])} {random.choice(['Doe', 'Smith', 'Brown'])}"
    address = f"{random.randint(100, 999)} {random.choice(['Elm', 'Maple', 'Oak'])} St"
    city = random.choice(["NY", "LA", "Chicago"])
    state = random.choice(["NY", "CA", "IL"])
    zip_code = str(random.randint(10000, 99999))
    card_number = ''.join(random.choices("1234567890", k=16))
    card_type = credentials.TestData.DEFAULT_CARD_TYPE
    exp_month = str(random.randint(1, 12)).zfill(2)
    exp_year = str(random.randint(2025, 2030))
    name_on_card = name

    logger.note(f"User Name: {name}")
    logger.note(f"Address: {address}, {city}, {state}, {zip_code}")
    logger.note(f"Card Type: {card_type}")
    logger.note(f"Card Number (Masked): **** **** **** {card_number[-4:]}")
    logger.note(f"Card Expiry: {exp_month}/{exp_year}")

    # Create Pydantic models
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
        name_on_card=name_on_card
    )

    booking_details = BookingDetails(
        flight_search=flight_search,
        passenger_info=passenger_info,
        payment_details=payment_details,
        remember_me=True
    )

    # Step 4: Fill in purchase form using Pydantic model
    logger.step("Filling out Purchase Form and Submitting")
    purchase.fill_booking_details(booking_details)
    purchase.submit_purchase()

    # Step 5: Confirmation page assertion
    logger.step("Validating Booking Confirmation Page")
    assert confirm.is_confirmation_successful(), "Booking confirmation failed!"
    confirmation_message = confirm.get_confirmation_message()
    logger.note(f"Confirmation Message: {confirmation_message}")
    logger.note("Booking completed successfully!")

    # Final Summary
    logger.summary(passed=1, failed=0, skipped=0)
