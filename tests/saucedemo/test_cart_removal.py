# tests/test_cart_removal.py

from playwright.sync_api import Page, expect
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage
from faker import Faker
import random

faker = Faker()


class TestCartRemoval:

    def test_remove_random_items_keep_backpack_or_fleece(self, page: Page):
        print("🧪 Starting: test_remove_random_items_keep_backpack_or_fleece")
        login = LoginPage(page)
        cart = CartPage(page)

        login.login_with_valid_credentials()

        # Step 1: Randomly choose one: Backpack or Fleece
        preferred_items = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"]
        chosen_item = random.choice(preferred_items)

        print(f"🎯 Adding either Backpack or Fleece: {chosen_item}")
        items = page.locator("div.inventory_item").all()
        for item in items:
            name = item.locator(".inventory_item_name").inner_text()
            if chosen_item in name:
                item.locator("button").click()
                break

        other_items = cart.add_random_items(count=2, exclude=[chosen_item])

        cart.go_to_cart()
        total_items = 1 + len(other_items)
        expect(page.locator(".shopping_cart_badge")).to_have_text(str(total_items))

        print(f"🦾 Removing 1 item: {other_items[0]}")
        cart.remove_item_by_name(other_items[0])

        page.wait_for_timeout(1000)
        remaining = cart.get_cart_items_names()
        print(f"✅ Remaining items: {remaining}")
        assert chosen_item in remaining

    def test_remove_all_items_from_cart(self, page: Page):
        print("🧼 Starting: test_remove_all_items_from_cart")
        login = LoginPage(page)
        cart = CartPage(page)

        login.login_with_valid_credentials()
        cart.add_random_items()
        cart.go_to_cart()
        cart.remove_all_items()

        assert len(cart.get_cart_items_names()) == 0
        print("✅ Cart is empty! 🧺")

    def test_complex_checkout_flow_add_then_finish(self, page: Page):
        print("🌀 Starting: test_complex_checkout_flow_add_then_finish")
        login = LoginPage(page)
        cart = CartPage(page)

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
        page.click("#cancel")  # return to inventory

        cart.add_item_by_index(1)
        cart.go_to_cart()
        cart.go_to_checkout()

        print(f"📦 Re-filling form for: {first_name} {last_name}, {postal_code}")
        cart.fill_checkout_form(first_name, last_name, postal_code)
        cart.complete_checkout()

        expect(page.locator("img[alt='Pony Express']")).to_be_visible()
        print(f"🎯 Complex checkout completed successfully for {first_name} {last_name}")
