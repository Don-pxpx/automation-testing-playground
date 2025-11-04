class HomePage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def open_homepage(self):
        self.page.goto("https://blazedemo.com")

    def select_departure_city(self, city_name):
        self.page.select_option("select[name='fromPort']", label=city_name)

    def select_destination_city(self, city_name):
        self.page.select_option("select[name='toPort']", label=city_name)

    def click_find_flights(self):
        self.page.click("input[type='submit']")
