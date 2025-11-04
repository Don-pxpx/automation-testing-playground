from playwright.sync_api import Page, expect
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage


class TestCart:

    def test_add_single_product_to_cart(self, page: Page):
        print("🛒 Starting: test_add_single_product_to_cart")
        login = LoginPage(page)
        cart = CartPage(page)

        login.login_with_valid_credentials()
        print("🧃 Adding first product to cart...")
        cart.add_item_by_index(0)

        print("🔢 Asserting cart count is 1...")
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")

        print("🧺 Navigating to cart page...")
        cart.go_to_cart()
        expect(page.locator("div.cart_item")).to_be_visible()
        print("✅ Cart has item! 🎯")

    def test_add_backpack_or_fleece_items_only_to_cart(self, page: Page):
        print("🎯 Starting: test_add_backpack_or_fleece_items_only_to_cart")
        login = LoginPage(page)
        cart = CartPage(page)

        login.login_with_valid_credentials()
        added_items = cart.add_backpack_and_fleece_only()
        expected_count = len(added_items)

        print(f"🔢 Expected cart count: {expected_count}")
        expect(page.locator(".shopping_cart_badge")).to_have_text(str(expected_count))

        cart.go_to_cart()
        cart_items = page.locator("div.cart_item").all()
        print(f"🧾 Items found in cart: {len(cart_items)}")
        assert len(cart_items) == expected_count
        print("✅ All selected items added correctly! 🎉")
