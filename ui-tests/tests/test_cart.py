import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_anadir_un_producto_al_carrito(inventory_page):
    inventory_page.add_to_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_have_text("1")


def test_anadir_varios_productos_aparecen_en_el_carrito(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.go_to_cart()
    cart = CartPage(inventory_page.page)

    expect(cart.cart_items).to_have_count(2)
    expect(cart.cart_items).to_contain_text([BACKPACK, BIKE_LIGHT])


def test_eliminar_producto_del_carrito(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.remove_from_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_be_hidden()
