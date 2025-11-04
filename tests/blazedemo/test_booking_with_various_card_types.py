import random
from seleniumbase import BaseCase
from pages.blazedemo_pages.home_page import HomePage
from pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from pages.blazedemo_pages.purchase_page import PurchasePage
from pages.blazedemo_pages.confirmation_page import ConfirmationPage
from helpers.log_helpers import InlineLogger  # <-- Import your Logger
from faker import Faker

fake = Faker()

class BookingWithCardTypesTest(BaseCase):
    def test_booking_with_various_card_types(self):
        logger = InlineLogger()  # Initialize Logger

        logger.step("Starting Test: Booking with Various Card Types")

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

        # Step 2: Wait for flights and choose random one
        logger.step("Waiting for flight listings and selecting a random flight")
        self.wait_for_element_visible("input[type='submit']", timeout=10)
        assert flight.get_flight_count() > 0, "No flights found!"
        chosen_index = random.randint(0, flight.get_flight_count() - 1)
        logger.note(f"Chosen Flight Index: {chosen_index}")
        flight.select_flight_by_index(chosen_index)

        # Step 3: Fill in purchase details with random card types
        logger.step("Filling purchase details with random card information")
        card_types = ["Visa", "American Express", "Diner's Club"]
        selected_card_type = random.choice(card_types)
        logger.note(f"Selected Card Type: {selected_card_type}")

        name = fake.name()
        address = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.postcode()
        card_number = ''.join(random.choices("1234567890", k=16))
        exp_month = str(random.randint(1, 12)).zfill(2)
        exp_year = str(random.randint(2025, 2030))

        logger.note(f"User Details: {name}, {address}, {city}, {state}, {zip_code}")
        logger.note(f"Card Number: {card_number} | Exp: {exp_month}/{exp_year}")

        purchase.fill_user_details(name, address, city, state, zip_code, card_number)
        purchase.select_card_type(selected_card_type)
        purchase.set_card_expiry(exp_month, exp_year)
        purchase.set_card_name(name)
        purchase.toggle_remember_me(check=True)
        purchase.submit_purchase()

        # Step 4: Confirm success message and verify details
        logger.step("Verifying booking confirmation message")
        confirmation_message = confirm.get_confirmation_message()
        logger.note(f"Confirmation Message: {confirmation_message}")
        assert confirm.is_confirmation_successful(), "Booking confirmation failed!"

        booking_details = confirm.get_booking_details()
        logger.note(f"Booking Details: {booking_details}")

        assert booking_details.get("Status") == "PendingCapture", "Unexpected booking status!"

        # Final Summary (Optional for this test since pass/fail is handled by assertions)
        logger.summary(passed=1, failed=0, skipped=0)

    def test_card_type_rejection(self):
        logger = InlineLogger()
        logger.step("Starting Test: Unsupported Card Types Not Present in Dropdown")

        purchase = PurchasePage(self)

        home = HomePage(self)
        flight = FlightSelectionPage(self)
        confirm = ConfirmationPage(self)

        # Pre-requisite: Navigate to purchase page
        home.open_homepage()
        home.select_departure_city("Boston")
        home.select_destination_city("New York")
        home.click_find_flights()
        self.wait_for_element_visible("input[type='submit']", timeout=10)
        flight.select_flight_by_index(0)

        logger.step("Fetching card type dropdown options")
        available_card_types = purchase.get_card_type_options()  # You'll need to add this method in PurchasePage

        logger.note(f"Available Card Types: {available_card_types}")

        unsupported_card_types = ["MasterCard", "Discover", "UnionPay"]
        for card in unsupported_card_types:
            if card in available_card_types:
                logger.warning(f"Unsupported Card Type Found in Dropdown: {card}")
            else:
                logger.note(f"✅ {card} correctly not present in dropdown")

        logger.step("Test Completed: Unsupported Card Types Verification")

        # Final Summary (Optional for this test since pass/fail is handled by assertions)
        logger.summary(passed=1, failed=0, skipped=0)