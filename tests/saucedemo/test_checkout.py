from seleniumbase import BaseCase
from faker import Faker
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage
from pages.saucedemo_pages.checkout_page import CheckoutPage
from helpers.log_helpers import InlineLogger  # 👈 Import logger

fake = Faker()

class CheckoutTests(BaseCase):

    def test_complete_checkout_single_item(self):
        logger = InlineLogger()
        logger.step("Starting Test: Complete Checkout with Single Item 🛒")

        login = LoginPage(self)
        cart = CartPage(self)
        checkout = CheckoutPage(self)

        logger.step("Logging in with valid credentials 🔐")
        login.login_with_valid_credentials()

        logger.step("Adding first item to cart 🧺")
        cart.add_item_by_index(0)
        cart.go_to_cart()

        logger.step("Proceeding to checkout 🚀")
        checkout.go_to_checkout()

        first = fake.first_name()
        last = fake.last_name()
        zip_code = fake.postcode()
        logger.note(f"Filling checkout form with: {first} {last}, {zip_code}")

        checkout.fill_checkout_form(first, last, zip_code)
        checkout.complete_checkout()

        self.assert_true(checkout.is_checkout_complete())
        logger.success("✅ Checkout completed successfully with Pony Express badge! 🎯")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_checkout_missing_info_shows_error(self):
        logger = InlineLogger()
        logger.step("Starting Test: Checkout Missing Info Should Show Error 🚨")

        login = LoginPage(self)
        cart = CartPage(self)
        checkout = CheckoutPage(self)

        logger.step("Logging in with valid credentials 🔐")
        login.login_with_valid_credentials()

        logger.step("Adding item to cart 🧺")
        cart.add_item_by_index(1)
        cart.go_to_cart()

        logger.step("Proceeding to checkout 🚪")
        checkout.go_to_checkout()

        logger.step("Submitting checkout form with missing info ⚠️")
        checkout.fill_checkout_form("", "", "")
        error_msg = checkout.get_error_text()

        self.assert_in("Error", error_msg)
        logger.error(f"❌ Error displayed as expected: {error_msg}")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_checkout_with_multiple_items(self):
        logger = InlineLogger()
        logger.step("Starting Test: Checkout Flow with Multiple Items 🛒📦")

        login = LoginPage(self)
        cart = CartPage(self)
        checkout = CheckoutPage(self)

        logger.step("Logging in with valid credentials 🔐")
        login.login_with_valid_credentials()

        logger.step("Adding 3 random items to cart 🎲")
        cart.add_random_items(count=3)
        cart.go_to_cart()

        logger.step("Proceeding to checkout 🚀")
        checkout.go_to_checkout()

        first = fake.first_name()
        last = fake.last_name()
        zip_code = fake.postcode()
        logger.note(f"Filling checkout form with: {first} {last}, {zip_code}")

        checkout.fill_checkout_form(first, last, zip_code)
        checkout.complete_checkout()

        self.assert_true(checkout.is_checkout_complete())
        logger.success(f"✅ Checkout completed successfully for {first} {last} 🎯")

        logger.summary(passed=1, failed=0, skipped=0)

    def test_checkout_cancel_and_return(self):
        logger = InlineLogger()
        logger.step("Starting Test: Cancel Checkout and Return to Inventory 🔁")

        login = LoginPage(self)
        cart = CartPage(self)
        checkout = CheckoutPage(self)

        logger.step("Logging in with valid credentials 🔐")
        login.login_with_valid_credentials()

        logger.step("Adding item to cart 🧺")
        cart.add_item_by_index(0)
        cart.go_to_cart()

        logger.step("Proceeding to checkout 🚪")
        checkout.go_to_checkout()

        first = fake.first_name()
        last = fake.last_name()
        zip_code = fake.postcode()
        logger.note(f"Filling checkout form with: {first} {last}, {zip_code}")

        logger.step("Cancelling checkout and returning to inventory ❌🔄")
        checkout.fill_checkout_form(first, last, zip_code)
        checkout.cancel_checkout()

        self.assert_element("div.inventory_item")
        logger.success("✅ Successfully returned to inventory page 🏠")

        logger.summary(passed=1, failed=0, skipped=0)
