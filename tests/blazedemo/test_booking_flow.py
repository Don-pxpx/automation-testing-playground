import random

from seleniumbase import BaseCase

from pages.blazedemo_pages.home_page import HomePage as HomePage
from pages.blazedemo_pages.flight_selection_page import FlightSelectionPage
from pages.blazedemo_pages.purchase_page import PurchasePage
from pages.blazedemo_pages.confirmation_page import ConfirmationPage
from config import credentials  # Assume you have default card type etc. here

class BookingFlowTests(BaseCase):
    def test_complete_booking_flow(self):
        print("\n🚀 Starting: test_complete_booking_flow")

        home = HomePage(self)
        flight = FlightSelectionPage(self)
        purchase = PurchasePage(self)
        confirm = ConfirmationPage(self)

        # Step 1: Visit Homepage and Select Cities
        home.open_homepage()
        home.select_departure_city("Boston")
        home.select_destination_city("New York")
        home.click_find_flights()

        # Step 2: Assert and choose random flight
        assert flight.get_flight_count() > 0
        print(f"✈️ Total flights found: {flight.get_flight_count()}")
        print("👀 First airline listed:", flight.get_airline_names()[0])

        chosen_index = random.randint(0, flight.get_flight_count() - 1)
        print(f"✈️ Choosing flight at index {chosen_index}")
        flight.select_flight_by_index(chosen_index)

        # Step 3: Generate random but valid user and card details
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

        # Step 4: Fill in purchase form
        purchase.fill_user_details(name, address, city, state, zip_code, card_number)
        purchase.select_card_type(card_type)
        purchase.set_card_expiry(exp_month, exp_year)
        purchase.set_card_name(name_on_card)
        purchase.toggle_remember_me()
        purchase.submit_purchase()

        # Step 5: Confirmation page assertion
        assert confirm.is_confirmation_successful()
        print("✅ Booking completed and confirmed!")

