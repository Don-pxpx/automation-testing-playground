from selenium.webdriver.common.by import By

class FlightSelectionPage:
    def __init__(self, base):
        self.base = base  # BaseCase instance

    def select_flight_by_index(self, index=0):
        flights = self.base.find_elements("input[type='submit']")
        if index < len(flights):
            flights[index].click()
        else:
            raise IndexError("❌ Not enough flights listed to select that index.")

    def get_flight_count(self):
        return len(self.base.find_elements("input[type='submit']"))

    def get_airline_names(self):
        rows = self.base.find_elements("table.table tbody tr")
        return [
            row.find_element(By.XPATH, "./td[3]").text  # 3rd column typically holds airline names
            for row in rows
        ]
