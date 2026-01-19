from playwright.sync_api import Page

class FlightSelectionPage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object

    def select_flight_by_index(self, index: int = 0):
        """Select a flight by its index."""
        flights = self.page.locator("input[type='submit']").all()
        if index < len(flights):
            flights[index].click()
        else:
            raise IndexError("❌ Not enough flights listed to select that index.")

    def get_flight_count(self) -> int:
        """Get the total number of available flights."""
        return len(self.page.locator("input[type='submit']").all())

    def get_airline_names(self) -> list[str]:
        """Get list of airline names from the flight table."""
        rows = self.page.locator("table.table tbody tr").all()
        airline_names = []
        for row in rows:
            # 3rd column typically holds airline names
            airline_cell = row.locator("td").nth(2)
            if airline_cell.is_visible():
                airline_names.append(airline_cell.text_content() or "")
        return airline_names
