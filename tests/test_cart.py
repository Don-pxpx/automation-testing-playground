from seleniumbase import BaseCase
from pages.login_page import LoginPage
from pages.cart_page import CartPage


class CartTests(BaseCase):

    def test_add_single_product_to_cart(self):
        print("🛒 Starting: test_add_single_product_to_cart")
        login = LoginPage(self)
        cart = CartPage(self)

        login.login_with_valid_credentials()
        print("🧃 Adding first product to cart...")
        cart.add_item_by_index(0)

        print("🔢 Asserting cart count is 1...")
        self.assert_text("1", ".shopping_cart_badge")

        print("🧺 Navigating to cart page...")
        cart.go_to_cart()
        self.assert_element("div.cart_item")
        print("✅ Cart has item! 🎯")

    def test_add_backpack_or_fleece_items_only_to_cart(self):
        print("🎯 Starting: test_add_backpack_or_fleece_items_only_to_cart")
        login = LoginPage(self)
        cart = CartPage(self)

        login.login_with_valid_credentials()
        added_items = cart.add_backpack_and_fleece_only()
        expected_count = len(added_items)

        print(f"🔢 Expected cart count: {expected_count}")
        self.assert_text(str(expected_count), ".shopping_cart_badge")

        cart.go_to_cart()
        cart_items = self.find_elements("div.cart_item")
        print(f"🧾 Items found in cart: {len(cart_items)}")
        self.assert_equal(len(cart_items), expected_count)
        print("✅ All selected items added correctly! 🎉")
