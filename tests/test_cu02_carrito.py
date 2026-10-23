"""CU-02 · Gestionar el carrito (RN-A4). Resultados esperados derivados de la ficha."""
from decimal import Decimal

import pytest
from carrito import Carrito

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
TODOS = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt",
         "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"]


@pytest.fixture
def carrito():
    return Carrito()


# Transición de estados: estado inicial VACÍO
def test_cu02_carrito_nuevo_esta_vacio(carrito):
    assert carrito.cantidad() == 0
    assert carrito.productos() == []
    assert carrito.subtotal() == Decimal("0.00")


# Partición de equivalencia: producto del catálogo (clase válida)
def test_cu02_agregar_producto_del_catalogo_lo_incluye(carrito):
    carrito.agregar(BACKPACK)
    assert carrito.productos() == [BACKPACK]
    assert carrito.cantidad() == 1


# Partición de equivalencia: productos fuera del catálogo (clases inválidas)
@pytest.mark.parametrize("producto", [
    "Sauce Labs Backpak",       # nombre mal escrito
    "sauce labs backpack",      # mayúsculas distintas
    "",                         # vacío
], ids=["mal_escrito", "mayusculas", "vacio"])
def test_cu02_agregar_producto_fuera_del_catalogo_es_rechazado(carrito, producto):
    with pytest.raises(ValueError):
        carrito.agregar(producto)
    assert carrito.cantidad() == 0


# Transición de estados: CON_PRODUCTOS + agregar el mismo producto → error, no se duplica
def test_cu02_agregar_producto_repetido_es_rechazado_y_no_se_duplica(carrito):
    carrito.agregar(BACKPACK)
    with pytest.raises(ValueError):
        carrito.agregar(BACKPACK)
    assert carrito.cantidad() == 1


# Transición de estados: quitar un producto presente → vuelve a VACÍO
def test_cu02_quitar_producto_presente_lo_elimina(carrito):
    carrito.agregar(BACKPACK)
    carrito.quitar(BACKPACK)
    assert carrito.cantidad() == 0
    assert carrito.subtotal() == Decimal("0.00")


# Transición inválida: quitar algo que no está en el carrito
@pytest.mark.parametrize("ya_en_carrito", [[], [BIKE_LIGHT]], ids=["carrito_vacio", "con_otro_producto"])
def test_cu02_quitar_producto_ausente_es_rechazado(carrito, ya_en_carrito):
    for p in ya_en_carrito:
        carrito.agregar(p)
    with pytest.raises(ValueError):
        carrito.quitar(BACKPACK)
    assert carrito.cantidad() == len(ya_en_carrito)


# Partición de equivalencia: subtotal con dos productos (29.99 + 9.99)
def test_cu02_subtotal_suma_los_precios_del_catalogo(carrito):
    carrito.agregar(BACKPACK)
    carrito.agregar(BIKE_LIGHT)
    assert carrito.subtotal() == Decimal("39.98")


# Valor límite: carrito lleno con los 6 productos del catálogo
def test_cu02_carrito_con_los_seis_productos(carrito):
    for p in TODOS:
        carrito.agregar(p)
    assert carrito.cantidad() == 6
    assert carrito.subtotal() == Decimal("129.94")
