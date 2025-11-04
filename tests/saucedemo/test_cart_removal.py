# tests/test_cart_removal.py

from playwright.sync_api import Page, expect
from pages.saucedemo_pages.login_page import LoginPage
from pages.saucedemo_pages.cart_page import CartPage
from helpers.log_helpers import InlineLogger
from faker import Faker
import random

faker = Faker()

def test_remove_random_items_keep_backpack_or_fleece(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Remove Random Items & Keep Backpack/Fleece 🎒🧥")

    login = LoginPage(page)
    cart = CartPage(page)

    logger.step("Logging in with valid credentials 🔐")
    login.login_with_valid_credentials()

    preferred_items = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"]
    chosen_item = random.choice(preferred_items)
    logger.note(f"Chosen Item to Retain: {chosen_item}")

    logger.step("Adding chosen item to cart 🛒")
    items = page.locator("div.inventory_item").all()
    for item in items:
        name = item.locator(".inventory_item_name").text_content()
        if name and chosen_item in name:
            item.locator("button").first.click()
            break

    logger.step("Adding 2 random additional items to cart 🎲")
    other_items = cart.add_random_items(count=2, exclude=[chosen_item])

    cart.go_to_cart()
    total_items = 1 + len(other_items)
    logger.note(f"Total items expected in cart: {total_items}")
    expect(page.locator(".shopping_cart_badge")).to_contain_text(str(total_items))

    logger.step(f"Removing 1 random item: {other_items[0]} ❌")
    cart.remove_item_by_name(other_items[0])

    page.wait_for_timeout(1000)
    remaining = cart.get_cart_items_names()
    logger.note(f"Remaining items in cart: {remaining}")
    assert chosen_item in remaining
    logger.success(f"✅ {chosen_item} is still present in the cart 🎯")

    logger.summary(passed=1, failed=0, skipped=0)

def test_remove_all_items_from_cart(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Remove All Items from Cart 🧹")

    login = LoginPage(page)
    cart = CartPage(page)

    logger.step("Logging in with valid credentials 🔐")
    login.login_with_valid_credentials()

    logger.step("Adding random items to cart 🛍️")
    cart.add_random_items()

    cart.go_to_cart()
    logger.step("Removing all items from cart 🗑️")
    cart.remove_all_items()

    remaining_items = cart.get_cart_items_names()
    assert len(remaining_items) == 0
    logger.success("✅ Cart is empty after removals! 🧺")

    logger.summary(passed=1, failed=0, skipped=0)

def test_complex_checkout_flow_add_then_finish(page: Page):
    logger = InlineLogger()
    logger.step("Starting Test: Complex Checkout Flow 🌀")

    login = LoginPage(page)
    cart = CartPage(page)

    logger.step("Logging in with valid credentials 🔐")
    login.login_with_valid_credentials()

    logger.step("Adding first item to cart 🛒")
    cart.add_item_by_index(0)

    cart.go_to_cart()
    cart.go_to_checkout()

    first_name = faker.first_name()
    last_name = faker.last_name()
    postal_code = faker.postcode()
    logger.note(f"Filling checkout form with: {first_name} {last_name}, {postal_code}")

    cart.fill_checkout_form(first_name, last_name, postal_code)
    page.click("#cancel")  # Returning to inventory page
    logger.step("Cancelled checkout, adding another item 🛍️")

    cart.add_item_by_index(1)
    cart.go_to_cart()
    cart.go_to_checkout()

    logger.step("Re-filling checkout form and completing purchase ✅")
    cart.fill_checkout_form(first_name, last_name, postal_code)
    cart.complete_checkout()

    expect(page.locator("img[alt='Pony Express']")).to_be_visible()
    logger.success(f"🎯 Complex checkout completed successfully for {first_name} {last_name}")

    logger.summary(passed=1, failed=0, skipped=0)
