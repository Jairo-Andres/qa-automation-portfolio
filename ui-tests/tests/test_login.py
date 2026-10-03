import re

import pytest
from playwright.sync_api import expect

from conftest import PASSWORD, STANDARD_USER
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_login_exitoso(login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    expect(login_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(InventoryPage(login_page.page).title).to_have_text("Products")


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
        (STANDARD_USER, "clave_incorrecta", "Username and password do not match"),
        ("", PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
    ],
    ids=["usuario_bloqueado", "password_incorrecto", "usuario_vacio", "password_vacio"],
)
def test_login_fallido(login_page, username, password, expected_error):
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(expected_error)
    expect(login_page.page).to_have_url(re.compile(r"saucedemo\.com/$"))
