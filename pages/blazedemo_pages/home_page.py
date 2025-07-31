class HomePage:
    def __init__(self, base):
        self.base = base  # SeleniumBase test class instance

    def open_homepage(self):
        self.base.open("https://blazedemo.com")

    def select_departure_city(self, city_name):
        self.base.select_option_by_text("select[name='fromPort']", city_name)

    def select_destination_city(self, city_name):
        self.base.select_option_by_text("select[name='toPort']", city_name)

    def click_find_flights(self):
        self.base.click("input[type='submit']")
