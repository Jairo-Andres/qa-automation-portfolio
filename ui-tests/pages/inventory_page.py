from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.sort_dropdown = page.locator(".product_sort_container")

    def _item(self, product_name: str):
        return self.items.filter(has_text=product_name)

    def add_to_cart(self, product_name: str):
        self._item(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str):
        self._item(product_name).get_by_role("button", name="Remove").click()

    def sort_by(self, option_value: str):
        """Valores: az, za, lohi, hilo."""
        self.sort_dropdown.select_option(option_value)

    def get_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def get_names(self) -> list[str]:
        return self.item_names.all_inner_texts()
