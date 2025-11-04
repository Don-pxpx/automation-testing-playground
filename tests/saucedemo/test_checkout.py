from playwright.sync_api import Page, expect
from faker import Faker
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage
from pages.saucedemo_pages.checkout_page import CheckoutPage


fake = Faker()


class TestCheckout:

    def test_complete_checkout_single_item(self, page: Page):
        print("🛒 Starting: test_complete_checkout_single_item")
        login = LoginPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)

        login.login_with_valid_credentials()
        cart.add_item_by_index(0)
        cart.go_to_cart()

        checkout.go_to_checkout()

        first = fake.first_name()
        last = fake.last_name()
        zip_code = fake.postcode()
        print(f"📝 Filling out form for: {first} {last}, {zip_code}")

        checkout.fill_checkout_form(first, last, zip_code)
        checkout.complete_checkout()

        assert checkout.is_checkout_complete()
        print("✅ Checkout finished with Pony Express badge! 🎯")

    def test_checkout_missing_info_shows_error(self, page: Page):
        print("🚨 Starting: test_checkout_missing_info_shows_error")
        login = LoginPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)

        login.login_with_valid_credentials()
        cart.add_item_by_index(1)
        cart.go_to_cart()
        checkout.go_to_checkout()

        checkout.fill_checkout_form("", "", "")
        error_msg = checkout.get_error_text()

        assert "Error" in error_msg
        print(f"❌ Error caught as expected: {error_msg}")

    def test_checkout_with_multiple_items(self, page: Page):
        print("🛒 Starting: test_checkout_with_multiple_items")
        login = LoginPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)

        login.login_with_valid_credentials()
        print("📦 Adding 3 random items to cart...")
        cart.add_random_items(count=3)
        cart.go_to_cart()

        print("🚀 Proceeding to checkout...")
        checkout.go_to_checkout()

        first = fake.first_name()
        last = fake.last_name()
        zip_code = fake.postcode()
        print(f"📝 Filling out form for: {first} {last}, {zip_code}")

        checkout.fill_checkout_form(first, last, zip_code)
        checkout.complete_checkout()

        assert checkout.is_checkout_complete()
        print("✅ Checkout finished with Pony Express badge! 🎯")

    def test_checkout_cancel_and_return(self, page: Page):
        print("🔁 Starting: test_checkout_cancel_and_return")
        login = LoginPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)

        login.login_with_valid_credentials()
        print("🧃 Adding 1 item to cart...")
        cart.add_item_by_index(0)
        cart.go_to_cart()

        print("🚪 Proceeding to checkout...")
        checkout.go_to_checkout()

        first = fake.first_name()
        last = fake.last_name()
        zip_code = fake.postcode()
        print(f"📝 Filling out form for: {first} {last}, {zip_code}")

        checkout.fill_checkout_form(first, last, zip_code)
        print("❌ Cancelling checkout and returning to inventory...")
        checkout.cancel_checkout()

        expect(page.locator("div.inventory_item")).to_be_visible()
        print("✅ Returned to inventory successfully! 🔄")
