# tests/test_cart_removal.py

from seleniumbase import BaseCase
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from faker import Faker
import random

faker = Faker()


class CartRemovalTests(BaseCase):

    def test_remove_random_items_keep_backpack_or_fleece(self):
        print("🧪 Starting: test_remove_random_items_keep_backpack_or_fleece")
        login = LoginPage(self)
        cart = CartPage(self)

        login.login_with_valid_credentials()

        # Step 1: Randomly choose one: Backpack or Fleece
        preferred_items = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"]
        chosen_item = random.choice(preferred_items)

        print(f"🎯 Adding either Backpack or Fleece: {chosen_item}")
        items = self.find_elements("div.inventory_item")
        for item in items:
            name = item.find_element("class name", "inventory_item_name").text
            if chosen_item in name:
                item.find_element("tag name", "button").click()
                break

        other_items = cart.add_random_items(count=2, exclude=[chosen_item])

        cart.go_to_cart()
        total_items = 1 + len(other_items)
        self.assert_text(str(total_items), ".shopping_cart_badge")

        print(f"🦾 Removing 1 item: {other_items[0]}")
        cart.remove_item_by_name(other_items[0])

        self.sleep(1)
        remaining = cart.get_cart_items_names()
        print(f"✅ Remaining items: {remaining}")
        self.assert_in(chosen_item, remaining)

    def test_remove_all_items_from_cart(self):
        print("🧼 Starting: test_remove_all_items_from_cart")
        login = LoginPage(self)
        cart = CartPage(self)

        login.login_with_valid_credentials()
        cart.add_random_items()
        cart.go_to_cart()
        cart.remove_all_items()

        self.assert_equal(len(cart.get_cart_items_names()), 0)
        print("✅ Cart is empty! 🧺")

    def test_complex_checkout_flow_add_then_finish(self):
        print("🌀 Starting: test_complex_checkout_flow_add_then_finish")
        login = LoginPage(self)
        cart = CartPage(self)

        login.login_with_valid_credentials()
        cart.add_item_by_index(0)

        cart.go_to_cart()
        cart.go_to_checkout()

        # 🧐 Use Faker for fake user details
        first_name = faker.first_name()
        last_name = faker.last_name()
        postal_code = faker.postcode()

        print(f"📝 Filling out form for: {first_name} {last_name}, {postal_code}")
        cart.fill_checkout_form(first_name, last_name, postal_code)
        self.click("#cancel")  # return to inventory

        cart.add_item_by_index(1)
        cart.go_to_cart()
        cart.go_to_checkout()

        print(f"📦 Re-filling form for: {first_name} {last_name}, {postal_code}")
        cart.fill_checkout_form(first_name, last_name, postal_code)
        cart.complete_checkout()

        self.assert_element("img[alt='Pony Express']")
        print(f"🎯 Complex checkout completed successfully for {first_name} {last_name}")
