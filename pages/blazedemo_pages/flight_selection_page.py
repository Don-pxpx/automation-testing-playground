class FlightSelectionPage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def select_flight_by_index(self, index=0):
        flights = self.page.locator("input[type='submit']").all()
        if index < len(flights):
            flights[index].click()
        else:
            raise IndexError("❌ Not enough flights listed to select that index.")

    def get_flight_count(self):
        return self.page.locator("input[type='submit']").count()

    def get_airline_names(self):
        rows = self.page.locator("table.table tbody tr").all()
        return [
            row.locator("td").nth(2).inner_text()  # 3rd column typically holds airline names
            for row in rows
        ]
