from seleniumbase import BaseCase
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage
from helpers.log_helpers import InlineLogger  # 👈 Import the logger

class CartTests(BaseCase):

    def test_add_single_product_to_cart(self):
        logger = InlineLogger()

        logger.step("Starting Test: Add Single Product to Cart 🛒")

        login = LoginPage(self)
        cart = CartPage(self)

        logger.step("Logging in with valid credentials 🔐")
        login.login_with_valid_credentials()

        logger.step("Adding first product to cart 🧃")
        cart.add_item_by_index(0)

        logger.step("Asserting cart count is 1 🔢")
        self.assert_text("1", ".shopping_cart_badge")
        logger.success("Cart badge count is correct (1 item)")

        logger.step("Navigating to cart page 🧺")
        cart.go_to_cart()
        self.assert_element("div.cart_item")
        logger.success("Cart page shows item successfully 🎯")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_add_backpack_or_fleece_items_only_to_cart(self):
        logger = InlineLogger()

        logger.step("Starting Test: Add Backpack or Fleece Items Only 🎯")

        login = LoginPage(self)
        cart = CartPage(self)

        logger.step("Logging in with valid credentials 🔐")
        login.login_with_valid_credentials()

        logger.step("Adding Backpack and Fleece items to cart 🎒🧥")
        added_items = cart.add_backpack_and_fleece_only()
        expected_count = len(added_items)

        logger.note(f"Expected cart count: {expected_count}")
        self.assert_text(str(expected_count), ".shopping_cart_badge")
        logger.success(f"Cart badge count is correct ({expected_count} items)")

        logger.step("Navigating to cart page 🧺")
        cart.go_to_cart()
        cart_items = self.find_elements("div.cart_item")

        logger.note(f"Items found in cart: {len(cart_items)}")
        self.assert_equal(len(cart_items), expected_count)
        logger.success("All selected items added correctly! 🎉")

        logger.summary(passed=1, failed=0, skipped=0)
