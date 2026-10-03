from playwright.sync_api import Page


class BasePage:
    """Clase base con lo que comparten todas las páginas."""

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def go_to_cart(self):
        self.cart_link.click()
