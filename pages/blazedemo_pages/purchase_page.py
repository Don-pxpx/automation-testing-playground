class PurchasePage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def fill_user_details(self, name, address, city, state, zip_code, card_number):
        self.page.fill("input#inputName", name)
        self.page.fill("input#address", address)
        self.page.fill("input#city", city)
        self.page.fill("input#state", state)
        self.page.fill("input#zipCode", zip_code)
        self.page.fill("input#creditCardNumber", card_number)

    def select_card_type(self, card_type):
        self.page.select_option("select#cardType", label=card_type)

    def set_card_expiry(self, month, year):
        self.page.fill("input#creditCardMonth", str(month))
        self.page.fill("input#creditCardYear", str(year))

    def set_card_name(self, name_on_card):
        self.page.fill("input#nameOnCard", name_on_card)

    def toggle_remember_me(self, check=True):
        checkbox = "input#rememberMe"
        if check and not self.page.locator(checkbox).is_checked():
            self.page.click(checkbox)
        elif not check and self.page.locator(checkbox).is_checked():
            self.page.click(checkbox)

    def submit_purchase(self):
        self.page.click("input[type='submit']")
