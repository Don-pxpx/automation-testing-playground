# pages/checkout_page.py

from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, base):
        self.base = base  # Inherited from BaseCase

    def go_to_checkout(self):
        self.base.click("#checkout")

    def fill_checkout_form(self, first, last, zip_code):
        self.base.type("#first-name", first)
        self.base.type("#last-name", last)
        self.base.type("#postal-code", zip_code)
        self.base.click("#continue")

    def complete_checkout(self):
        self.base.click("#finish")

    def cancel_checkout(self):
        self.base.click("#cancel")

    def is_checkout_complete(self):
        return self.base.is_element_visible("img[alt='Pony Express']")

    def get_error_text(self):
        return self.base.get_text("h3[data-test='error']")
