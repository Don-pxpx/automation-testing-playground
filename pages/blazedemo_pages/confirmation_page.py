from selenium.webdriver.common.by import By


class ConfirmationPage:
    def __init__(self, base):
        self.base = base  # SeleniumBase test class instance

    def get_booking_details(self):
        rows = self.base.find_elements("table tr")
        details = {}
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                key = cells[0].text.strip(":")
                value = cells[1].text
                details[key] = value
        return details

    def get_confirmation_message(self):
        self.base.wait_for_element("h1", timeout=10)  # Explicit wait
        return self.base.get_text("h1")

    def is_confirmation_successful(self):
        return "Thank you for your purchase today!" in self.get_confirmation_message()

