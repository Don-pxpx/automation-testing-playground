from playwright.sync_api import Page

class ConfirmationPage:
    def __init__(self, page: Page):
        self.page = page  # Playwright page object

    def get_booking_details(self) -> dict[str, str]:
        """Get booking details from the confirmation table."""
        rows = self.page.locator("table tr").all()
        details = {}
        for row in rows:
            cells = row.locator("td").all()
            if len(cells) == 2:
                key = (cells[0].text_content() or "").strip(":")
                value = cells[1].text_content() or ""
                details[key] = value
        return details

    def get_confirmation_message(self) -> str:
        """Get the confirmation message from the page."""
        self.page.wait_for_selector("h1", timeout=10000)
        return self.page.locator("h1").text_content() or ""

    def is_confirmation_successful(self) -> bool:
        """Check if booking confirmation was successful."""
        return "Thank you for your purchase today!" in self.get_confirmation_message()
