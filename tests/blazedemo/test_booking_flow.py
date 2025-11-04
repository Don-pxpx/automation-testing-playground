import random
from seleniumbase import BaseCase

from pages.blazedemo_pages.home_page import HomePage
from pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from pages.blazedemo_pages.purchase_page import PurchasePage
from pages.blazedemo_pages.confirmation_page import ConfirmationPage
from config import credentials  # Assume you have default card type etc. here
from helpers.log_helpers import InlineLogger  # Importing the logger helper

class BookingFlowTests(BaseCase):
    def test_complete_booking_flow(self):
        logger = InlineLogger()
        logger.step("Starting Test: Complete Booking Flow")

        home = HomePage(self)
        flight = FlightSelectionPage(self)
        purchase = PurchasePage(self)
        confirm = ConfirmationPage(self)

        # Step 1: Navigate to homepage and select cities randomly
        logger.step("Navigating to BlazeDemo homepage and selecting cities")
        departure_cities = ["Boston", "Philadelphia", "Portland", "San Diego", "Mexico City", "São Paolo"]
        destination_cities = ["New York", "Berlin", "Rome", "London"]

        departure_city = random.choice(departure_cities)
        destination_city = random.choice([city for city in destination_cities if city != departure_city])

        logger.note(f"Selected Departure City: {departure_city}")
        logger.note(f"Selected Destination City: {destination_city}")

        home.open_homepage()
        self.wait_for_element_visible("select[name='fromPort']", timeout=10)
        home.select_departure_city(departure_city)
        home.select_destination_city(destination_city)
        home.click_find_flights()

        # Step 2: Assert and choose random flight
        logger.step("Waiting for available flights and selecting a random flight")
        self.wait_for_element_visible("input[type='submit']", timeout=10)
        flight_count = flight.get_flight_count()
        assert flight_count > 0, "No flights found!"
        logger.note(f"Total Flights Found: {flight_count}")
        logger.note(f"First Airline Listed: {flight.get_airline_names()[0]}")

        chosen_index = random.randint(0, flight_count - 1)
        logger.note(f"Chosen Flight Index: {chosen_index}")
        flight.select_flight_by_index(chosen_index)

        # Step 3: Generate random but valid user and card details
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

        # Step 4: Fill in purchase form
        logger.step("Filling out Purchase Form and Submitting")
        purchase.fill_user_details(name, address, city, state, zip_code, card_number)
        purchase.select_card_type(card_type)
        purchase.set_card_expiry(exp_month, exp_year)
        purchase.set_card_name(name_on_card)
        purchase.toggle_remember_me()
        purchase.submit_purchase()

        # Step 5: Confirmation page assertion
        logger.step("Validating Booking Confirmation Page")
        assert confirm.is_confirmation_successful(), "Booking confirmation failed!"
        confirmation_message = confirm.get_confirmation_message()
        logger.note(f"Confirmation Message: {confirmation_message}")
        logger.note("Booking completed successfully!")

        # Final Summary (for visual wrap-up)
        logger.summary(passed=1, failed=0, skipped=0)

