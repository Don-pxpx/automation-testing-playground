from dataclasses import dataclass

from playwright.sync_api import Page

from automation_testing_playground.pages.saucedemo_pages.cart_page import CartPage
from automation_testing_playground.pages.saucedemo_pages.checkout_page import CheckoutPage


@dataclass(frozen=True)
class CustomerInfo:
    first_name: str
    last_name: str
    postal_code: str


class CheckoutFlow:
    """SauceDemo shopper journey: cart → checkout → confirmation."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart = CartPage(page)
        self.checkout = CheckoutPage(page)

    def complete_single_item_checkout(self, customer: CustomerInfo) -> None:
        self.cart.add_item_by_index(0)
        self.cart.go_to_cart()
        self.checkout.go_to_checkout()
        self.checkout.fill_checkout_form(
            customer.first_name,
            customer.last_name,
            customer.postal_code,
        )
        self.checkout.complete_checkout()
        if not self.checkout.is_checkout_complete():
            raise AssertionError("Checkout did not reach confirmation page")

    def complete_multi_item_checkout(self, customer: CustomerInfo, item_count: int = 3) -> None:
        self.cart.add_random_items(count=item_count)
        self.cart.go_to_cart()
        self.checkout.go_to_checkout()
        self.checkout.fill_checkout_form(
            customer.first_name,
            customer.last_name,
            customer.postal_code,
        )
        self.checkout.complete_checkout()
        if not self.checkout.is_checkout_complete():
            raise AssertionError("Multi-item checkout did not reach confirmation page")

    def cancel_checkout_and_return_to_inventory(self, customer: CustomerInfo) -> None:
        self.cart.add_item_by_index(0)
        self.cart.go_to_cart()
        self.checkout.go_to_checkout()
        self.checkout.fill_checkout_form(
            customer.first_name,
            customer.last_name,
            customer.postal_code,
        )
        self.checkout.cancel_checkout()
