# pages/checkout_page.py

from playwright.sync_api import expect

class CheckoutPage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def go_to_checkout(self):
        self.page.click("#checkout")

    def fill_checkout_form(self, first, last, zip_code):
        self.page.fill("#first-name", first)
        self.page.fill("#last-name", last)
        self.page.fill("#postal-code", zip_code)
        self.page.click("#continue")

    def complete_checkout(self):
        self.page.click("#finish")

    def cancel_checkout(self):
        self.page.click("#cancel")

    def is_checkout_complete(self):
        return self.page.locator("img[alt='Pony Express']").is_visible()

    def get_error_text(self):
        return self.page.locator("h3[data-test='error']").text_content() or ""
