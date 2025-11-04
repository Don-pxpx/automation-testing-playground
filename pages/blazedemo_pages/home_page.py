class HomePage:
    def __init__(self, base):
        self.base = base  # SeleniumBase test class instance

    def open_homepage(self):
        # Try HTTPS first, then fall back to HTTP if elements don't load quickly
        self.base.open("https://blazedemo.com")
        try:
            self.base.wait_for_element_present("select[name='fromPort']", timeout=7)
        except Exception:
            self.base.open("http://blazedemo.com")
            self.base.wait_for_element_present("select[name='fromPort']", timeout=12)

    def select_departure_city(self, city_name):
        self.base.wait_for_element_present("select[name='fromPort']", timeout=10)
        self.base.select_option_by_text("select[name='fromPort']", city_name)

    def select_destination_city(self, city_name):
        self.base.wait_for_element_present("select[name='toPort']", timeout=10)
        self.base.select_option_by_text("select[name='toPort']", city_name)

    def click_find_flights(self):
        self.base.click("input[type='submit']")
