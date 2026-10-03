import re

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.smoke
def test_compra_completa_e2e(inventory_page):
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    CartPage(inventory_page.page).checkout()

    checkout = CheckoutPage(inventory_page.page)
    checkout.fill_info("Ana", "García", "28001")

    expect(checkout.title).to_have_text("Checkout: Overview")
    expect(checkout.total_label).to_contain_text("$")

    checkout.finish()

    expect(checkout.page).to_have_url(re.compile(r"/checkout-complete\.html$"))
    expect(checkout.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "García", "28001", "First Name is required"),
        ("Ana", "", "28001", "Last Name is required"),
        ("Ana", "García", "", "Postal Code is required"),
    ],
    ids=["sin_nombre", "sin_apellido", "sin_codigo_postal"],
)
def test_checkout_con_datos_incompletos(inventory_page, first_name, last_name, postal_code, expected_error):
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    CartPage(inventory_page.page).checkout()

    checkout = CheckoutPage(inventory_page.page)
    checkout.fill_info(first_name, last_name, postal_code)

    expect(checkout.error_message).to_contain_text(expected_error)
