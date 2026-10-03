import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# Usuarios públicos de prueba de saucedemo.com (aparecen en la propia web)
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    """Deja al usuario logueado en la página de productos."""
    login_page.login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(login_page.page)
    expect(inventory.title).to_have_text("Products")
    return inventory
