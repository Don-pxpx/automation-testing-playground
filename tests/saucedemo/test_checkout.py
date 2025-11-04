from playwright.sync_api import Page, expect
from faker import Faker
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage
from pages.saucedemo_pages.checkout_page import CheckoutPage
from helpers.log_helpers import InlineLogger

fake = Faker()

def test_complete_checkout_single_item(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Complete Checkout with Single Item 🛒")

    login = LoginPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

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

    assert checkout.is_checkout_complete()
    logger.success("✅ Checkout completed successfully with Pony Express badge! 🎯")

    logger.summary(passed=1, failed=0, skipped=0)

def test_checkout_missing_info_shows_error(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Checkout Missing Info Should Show Error 🚨")

    login = LoginPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

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

    assert "Error" in error_msg
    logger.error(f"❌ Error displayed as expected: {error_msg}")

    logger.summary(passed=1, failed=0, skipped=0)

def test_checkout_with_multiple_items(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Checkout Flow with Multiple Items 🛒📦")

    login = LoginPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

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

    assert checkout.is_checkout_complete()
    logger.success(f"✅ Checkout completed successfully for {first} {last} 🎯")

    logger.summary(passed=1, failed=0, skipped=0)

def test_checkout_cancel_and_return(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Cancel Checkout and Return to Inventory 🔁")

    login = LoginPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

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

    expect(page.locator("div.inventory_item").first).to_be_visible()
    logger.success("✅ Successfully returned to inventory page 🏠")

    logger.summary(passed=1, failed=0, skipped=0)
