class ConfirmationPage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def get_booking_details(self):
        rows = self.page.locator("table tr").all()
        details = {}
        for row in rows:
            cells = row.locator("td").all()
            if len(cells) == 2:
                key = cells[0].inner_text().strip(":")
                value = cells[1].inner_text()
                details[key] = value
        return details

    def get_confirmation_message(self):
        return self.page.locator("h1").inner_text()

    def is_confirmation_successful(self):
        return "Thank you for your purchase today!" in self.get_confirmation_message()
