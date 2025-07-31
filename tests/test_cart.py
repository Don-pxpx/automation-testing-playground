from seleniumbase import BaseCase
from config.credentials import TestData
from selenium.webdriver.common.by import By


class CartTests(BaseCase):

    def test_add_single_product_to_cart(self):
        print("🛒 Starting: test_add_single_product_to_cart")
        self.open(TestData.BASE_URL)
        print("🔐 Logging in with valid credentials...")
        self.type("#user-name", TestData.VALID_USER)
        self.type("#password", TestData.VALID_PASSWORD)
        self.click("#login-button")

        print("🧃 Adding first product to cart...")
        self.click("button.btn_inventory")  # adds the first item

        print("🔢 Asserting cart count is 1...")
        self.assert_text("1", ".shopping_cart_badge")

        print("🧺 Navigating to cart page...")
        self.click(".shopping_cart_link")
        self.assert_element("div.cart_item")
        print("✅ Cart has item! 🎯")

    def test_add_backpack_or_fleece_items_only_to_cart(self):
        print("🎯 Starting: test_add_backpack_or_fleece_items_only_to_cart")
        self.open(TestData.BASE_URL)
        print("🔐 Logging in...")
        self.type("#user-name", TestData.VALID_USER)
        self.type("#password", TestData.VALID_PASSWORD)
        self.click("#login-button")

        print("🔎 Scanning for a backpack or fleece products...")
        item_count = 0
        products = self.find_elements("div.inventory_item")

        for product in products:
            name = product.find_element(By.CSS_SELECTOR, "div.inventory_item_name").text.lower()
            desc = product.find_element(By.CSS_SELECTOR, "div.inventory_item_desc").text.lower()

            if "backpack" in name or "fleece" in name:
                print(f"🎯 Adding: {name}")
                product.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
                item_count += 1

        print(f"🔢 Expected cart count: {item_count}")
        self.assert_text(str(item_count), ".shopping_cart_badge")

        print("🧺 Navigating to cart page...")
        self.click(".shopping_cart_link")
        cart_items = self.find_elements("div.cart_item")
        print(f"🧾 Items found in cart: {len(cart_items)}")
        self.assert_equal(len(cart_items), item_count)

        print("✅ All black items added correctly! 🎉")
