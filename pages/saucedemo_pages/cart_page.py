# pages/cart_page.py

from selenium.webdriver.common.by import By
import random

class CartPage:
    def __init__(self, base):
        self.base = base  # BaseCase from test

    def add_item_by_index(self, index):
        items = self.base.find_elements("div.inventory_item")
        if index < len(items):
            items[index].find_element(By.TAG_NAME, "button").click()

    def add_backpack_and_fleece_only(self):
        items = self.base.find_elements("div.inventory_item")
        selected = []

        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if "Backpack" in name or "Fleece" in name:
                item.find_element(By.TAG_NAME, "button").click()
                selected.append(name)
        return selected

    def add_random_items(self, count=2, exclude=None):
        if exclude is None:
            exclude = []
        items = self.base.find_elements("div.inventory_item")
        available = []

        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name not in exclude:
                available.append((item, name))

        random.shuffle(available)
        selected_items = available[:count]
        selected_names = []

        for item, name in selected_items:
            item.find_element(By.TAG_NAME, "button").click()
            selected_names.append(name)

        return selected_names

    def go_to_cart(self):
        self.base.click(".shopping_cart_link")

    def remove_item_by_name(self, item_name):
        items = self.base.find_elements("div.cart_item")
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == item_name:
                item.find_element(By.TAG_NAME, "button").click()
                break

    def get_cart_items_names(self):
        items = self.base.find_elements("div.cart_item")
        return [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in items]

    def remove_all_items(self):
        buttons = self.base.find_elements("button")
        for btn in buttons:
            if btn.text == "Remove":
                btn.click()

    def go_to_checkout(self):
        self.base.click("#checkout")

    def fill_checkout_form(self, first, last, zip_code):
        self.base.type("#first-name", first)
        self.base.type("#last-name", last)
        self.base.type("#postal-code", zip_code)
        self.base.click("#continue")

    def complete_checkout(self):
        self.base.click("#finish")
