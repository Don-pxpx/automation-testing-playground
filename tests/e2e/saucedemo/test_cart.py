from playwright.sync_api import Page, expect

from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.cart_page import CartPage


def test_add_single_product_to_cart(logged_in_inventory: CartPage):
    """SDC-CART-001: One product added; cart badge and cart page reflect item (correctness)."""
    logger = InlineLogger()
    cart = logged_in_inventory
    page = cart.page

    logger.step("Starting Test: Add Single Product to Cart 🛒")

    logger.step("Adding first product to cart 🧃")
    cart.add_item_by_index(0)

    logger.step("Asserting cart count is 1 🔢")
    expect(page.locator(".shopping_cart_badge")).to_contain_text("1")
    logger.success("Cart badge count is correct (1 item)")

    logger.step("Navigating to cart page 🧺")
    cart.go_to_cart()
    expect(page.locator("div.cart_item")).to_be_visible()
    logger.success("Cart page shows item successfully 🎯")

    logger.summary(passed=1, failed=0, skipped=0)


def test_add_backpack_or_fleece_items_only_to_cart(logged_in_inventory: CartPage):
    """SDC-CART-002: Only backpack and fleece can be added together (completeness)."""
    logger = InlineLogger()
    cart = logged_in_inventory
    page = cart.page

    logger.step("Starting Test: Add Backpack or Fleece Items Only 🎯")

    logger.step("Adding Backpack and Fleece items to cart 🎒🧥")
    added_items = cart.add_backpack_and_fleece_only()
    expected_count = len(added_items)

    logger.note(f"Expected cart count: {expected_count}")
    expect(page.locator(".shopping_cart_badge")).to_contain_text(str(expected_count))
    logger.success(f"Cart badge count is correct ({expected_count} items)")

    logger.step("Navigating to cart page 🧺")
    cart.go_to_cart()
    cart_items = page.locator("div.cart_item").all()

    logger.note(f"Items found in cart: {len(cart_items)}")
    assert len(cart_items) == expected_count
    logger.success("All selected items added correctly! 🎉")

    logger.summary(passed=1, failed=0, skipped=0)
