# pages/cart_page.py

import random

class CartPage:
    def __init__(self, page):
        self.page = page  # Playwright page object

    def add_item_by_index(self, index):
        items = self.page.locator("div.inventory_item").all()
        if index < len(items):
            items[index].locator("button").first.click()

    def add_backpack_and_fleece_only(self):
        items = self.page.locator("div.inventory_item").all()
        selected = []

        for item in items:
            name = item.locator(".inventory_item_name").text_content()
            if name and ("Backpack" in name or "Fleece" in name):
                item.locator("button").first.click()
                selected.append(name)
        return selected

    def add_random_items(self, count=2, exclude=None):
        if exclude is None:
            exclude = []
        items = self.page.locator("div.inventory_item").all()
        available = []

        for item in items:
            name = item.locator(".inventory_item_name").text_content()
            if name and name not in exclude:
                available.append((item, name))

        random.shuffle(available)
        selected_items = available[:count]
        selected_names = []

        for item, name in selected_items:
            item.locator("button").first.click()
            selected_names.append(name)

        return selected_names

    def go_to_cart(self):
        self.page.click(".shopping_cart_link")

    def remove_item_by_name(self, item_name):
        items = self.page.locator("div.cart_item").all()
        for item in items:
            name = item.locator(".inventory_item_name").text_content()
            if name == item_name:
                item.locator("button").first.click()
                break

    def get_cart_items_names(self):
        items = self.page.locator("div.cart_item").all()
        return [item.locator(".inventory_item_name").text_content() for item in items]

    def remove_all_items(self):
        buttons = self.page.locator("button").all()
        for btn in buttons:
            if btn.text_content() == "Remove":
                btn.click()

    def go_to_checkout(self):
        self.page.click("#checkout")

    def fill_checkout_form(self, first, last, zip_code):
        self.page.fill("#first-name", first)
        self.page.fill("#last-name", last)
        self.page.fill("#postal-code", zip_code)
        self.page.click("#continue")

    def complete_checkout(self):
        self.page.click("#finish")
