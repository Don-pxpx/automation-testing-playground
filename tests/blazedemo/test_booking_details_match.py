import random
from faker import Faker
from seleniumbase import BaseCase
from helpers.log_helpers import InlineLogger  # Importing the logger helper

from pages.blazedemo_pages.home_page import HomePage
from pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from pages.blazedemo_pages.purchase_page import PurchasePage
from pages.blazedemo_pages.confirmation_page import ConfirmationPage

fake = Faker()

class BookingDetailMatchTest(BaseCase):
    def test_booking_details_match(self):
        logger = InlineLogger()
        logger.step("Starting Test: Booking Details Match")

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
        home.select_departure_city(departure_city)
        home.select_destination_city(destination_city)
        home.click_find_flights()

        # Step 2: Choose a random flight
        logger.step("Waiting for flight listings and selecting a random flight")
        self.wait_for_element_visible("input[type='submit']", timeout=10)
        flight_count = flight.get_flight_count()
        assert flight_count > 0, "No flights available!"
        chosen_index = random.randint(0, flight_count - 1)
        logger.note(f"Chosen Flight Index: {chosen_index}")
        flight.select_flight_by_index(chosen_index)

        # Step 3: Fill in user and payment details
        logger.step("Filling purchase details with random user and card information")
        name = fake.name()
        address = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.postcode()
        card_number = ''.join(random.choices("1234567890", k=16))
        card_type = "Visa"
        exp_month = str(random.randint(1, 12)).zfill(2)
        exp_year = str(random.randint(2025, 2030))

        logger.note(f"User Details: {name}, {address}, {city}, {state}, {zip_code}")
        logger.note(f"Card Number: {card_number} | Card Type: {card_type} | Expiry: {exp_month}/{exp_year}")

        purchase.fill_user_details(name, address, city, state, zip_code, card_number)
        purchase.select_card_type(card_type)
        purchase.set_card_expiry(exp_month, exp_year)
        purchase.set_card_name(name)
        purchase.toggle_remember_me(check=True)
        purchase.submit_purchase()

        # Step 4: Extract confirmation details and validate
        logger.step("Verifying booking confirmation message and booking details")
        confirmation_message = confirm.get_confirmation_message()
        logger.note(f"Confirmation Message: {confirmation_message}")
        assert confirm.is_confirmation_successful(), "Booking confirmation failed!"

        booking_details = confirm.get_booking_details()
        logger.note(f"Booking Details: {booking_details}")

        # Assertions (with inline logging if failed)
        try:
            assert "USD" in booking_details.get("Amount", ""), "Amount missing or incorrect!"
        except AssertionError as e:
            logger.error(str(e))
            raise

        try:
            assert booking_details.get("Status") == "PendingCapture", "Unexpected booking status!"
        except AssertionError as e:
            logger.error(str(e))
            raise

        try:
            assert booking_details.get("Card Number").endswith("1111"), "Card number mismatch!"  # BlazeDemo hardcoded
        except AssertionError as e:
            logger.error(str(e))
            raise

        # Final Summary
        logger.summary(passed=1, failed=0, skipped=0)
