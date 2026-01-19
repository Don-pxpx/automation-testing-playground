from playwright.sync_api import Page
from automation_testing_playground.models.blazedemo_models import FlightSearch

class HomePage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object

    def open_homepage(self):
        """Open BlazeDemo homepage."""
        # Try HTTPS first, then fall back to HTTP if elements don't load quickly
        self.page.goto("https://blazedemo.com")
        try:
            self.page.wait_for_selector("select[name='fromPort']", timeout=7000)
        except Exception:
            self.page.goto("http://blazedemo.com")
            self.page.wait_for_selector("select[name='fromPort']", timeout=12000)

    def select_departure_city(self, city_name: str):
        """Select departure city from dropdown."""
        self.page.wait_for_selector("select[name='fromPort']", timeout=10000)
        self.page.select_option("select[name='fromPort']", label=city_name)

    def select_destination_city(self, city_name: str):
        """Select destination city from dropdown."""
        self.page.wait_for_selector("select[name='toPort']", timeout=10000)
        self.page.select_option("select[name='toPort']", label=city_name)

    def select_flight_search(self, flight_search: FlightSearch):
        """Select flight search using Pydantic model."""
        self.select_departure_city(flight_search.departure_city)
        self.select_destination_city(flight_search.destination_city)

    def click_find_flights(self):
        """Click the Find Flights button."""
        self.page.click("input[type='submit']")
