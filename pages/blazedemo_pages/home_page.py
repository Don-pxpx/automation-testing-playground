class HomePage:
    def __init__(self, base):
        self.base = base  # SeleniumBase test class instance

    def open_homepage(self):
        self.base.open("https://blazedemo.com")
        # Wait for the route dropdown to be present to ensure page is ready
        self.base.wait_for_element_visible("select[name='fromPort']", timeout=15)

    def select_departure_city(self, city_name):
        self.base.wait_for_element_present("select[name='fromPort']", timeout=10)
        self.base.select_option_by_text("select[name='fromPort']", city_name)

    def select_destination_city(self, city_name):
        self.base.wait_for_element_present("select[name='toPort']", timeout=10)
        self.base.select_option_by_text("select[name='toPort']", city_name)

    def click_find_flights(self):
        self.base.click("input[type='submit']")
