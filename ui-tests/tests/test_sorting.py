from playwright.sync_api import expect


def test_ordenar_por_precio_de_menor_a_mayor(inventory_page):
    inventory_page.sort_by("lohi")
    expect(inventory_page.sort_dropdown).to_have_value("lohi")

    prices = inventory_page.get_prices()

    assert prices == sorted(prices)


def test_ordenar_por_precio_de_mayor_a_menor(inventory_page):
    inventory_page.sort_by("hilo")
    expect(inventory_page.sort_dropdown).to_have_value("hilo")

    prices = inventory_page.get_prices()

    assert prices == sorted(prices, reverse=True)


def test_ordenar_por_nombre_z_a(inventory_page):
    inventory_page.sort_by("za")
    expect(inventory_page.sort_dropdown).to_have_value("za")

    names = inventory_page.get_names()

    assert names == sorted(names, reverse=True)
