class PurchasePage:
    def __init__(self, base):
        self.base = base  # SeleniumBase test class instance

    def fill_user_details(self, name, address, city, state, zip_code, card_number):
        # Ensure purchase form is loaded
        self.base.wait_for_element_visible("input#inputName", timeout=15)
        self.base.type("input#inputName", name)
        self.base.type("input#address", address)
        self.base.type("input#city", city)
        self.base.type("input#state", state)
        self.base.type("input#zipCode", zip_code)
        self.base.type("input#creditCardNumber", card_number)

    def select_card_type(self, card_type):
        self.base.select_option_by_text("select#cardType", card_type)

    def set_card_expiry(self, month, year):
        self.base.type("input#creditCardMonth", str(month))
        self.base.type("input#creditCardYear", str(year))

    def set_card_name(self, name_on_card):
        self.base.type("input#nameOnCard", name_on_card)

    def toggle_remember_me(self, check=True):
        checkbox = "input#rememberMe"
        if check and not self.base.is_selected(checkbox):
            self.base.click(checkbox)
        elif not check and self.base.is_selected(checkbox):
            self.base.click(checkbox)

    def submit_purchase(self):
        self.base.click("input[type='submit']")

    def get_card_type_options(self):
        return [option.text for option in self.base.find_elements("select#cardType option")]
