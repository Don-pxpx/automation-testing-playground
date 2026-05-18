from faker import Faker
from playwright.sync_api import expect

from automation_testing_playground.flows.saucedemo_checkout_flow import CheckoutFlow, CustomerInfo
from automation_testing_playground.helpers.log_helpers import InlineLogger
from automation_testing_playground.pages.saucedemo_pages.cart_page import CartPage
from automation_testing_playground.pages.saucedemo_pages.checkout_page import CheckoutPage

fake = Faker()


def test_complete_checkout_single_item(logged_in_inventory: CartPage):
    """SDC-CHKO-001: Single-item checkout reaches confirmation (functional correctness)."""
    logger = InlineLogger()
    page = logged_in_inventory.page
    logger.step("Starting Test: Complete Checkout with Single Item 🛒")

    customer = CustomerInfo(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        postal_code=fake.postcode(),
    )
    logger.note(f"Filling checkout form with: {customer.first_name} {customer.last_name}, {customer.postal_code}")

    CheckoutFlow(page).complete_single_item_checkout(customer)
    logger.success("✅ Checkout completed successfully with Pony Express badge! 🎯")
    logger.summary(passed=1, failed=0, skipped=0)


def test_checkout_missing_info_shows_error(logged_in_inventory: CartPage):
    """SDC-CHKO-002: Checkout with empty customer fields shows error (functional correctness)."""
    logger = InlineLogger()
    cart = logged_in_inventory
    checkout = CheckoutPage(cart.page)

    logger.step("Starting Test: Checkout Missing Info Should Show Error 🚨")
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


def test_checkout_with_multiple_items(logged_in_inventory: CartPage):
    """SDC-CHKO-003: Multi-item checkout completes successfully (functional completeness)."""
    logger = InlineLogger()
    page = logged_in_inventory.page
    customer = CustomerInfo(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        postal_code=fake.postcode(),
    )

    logger.step("Starting Test: Checkout Flow with Multiple Items 🛒📦")
    CheckoutFlow(page).complete_multi_item_checkout(customer, item_count=3)
    assert CheckoutPage(page).is_checkout_complete()
    logger.success(f"✅ Checkout completed successfully for {customer.first_name} {customer.last_name} 🎯")
    logger.summary(passed=1, failed=0, skipped=0)


def test_checkout_cancel_and_return(logged_in_inventory: CartPage):
    """SDC-CHKO-004: Cancel checkout returns shopper to inventory (functional appropriateness)."""
    logger = InlineLogger()
    page = logged_in_inventory.page
    customer = CustomerInfo(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        postal_code=fake.postcode(),
    )

    logger.step("Starting Test: Cancel Checkout and Return to Inventory 🔁")
    CheckoutFlow(page).cancel_checkout_and_return_to_inventory(customer)
    expect(page.locator("div.inventory_item").first).to_be_visible()
    logger.success("✅ Successfully returned to inventory page 🏠")
    logger.summary(passed=1, failed=0, skipped=0)
