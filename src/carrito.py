"""CU-02 · Gestionar el carrito (RN-A4)."""
from decimal import Decimal

CATALOGO = {
    "Sauce Labs Backpack": Decimal("29.99"),
    "Sauce Labs Bike Light": Decimal("9.99"),
    "Sauce Labs Bolt T-Shirt": Decimal("15.99"),
    "Sauce Labs Fleece Jacket": Decimal("49.99"),
    "Sauce Labs Onesie": Decimal("7.99"),
    "Test.allTheThings() T-Shirt (Red)": Decimal("15.99"),
}


class Carrito:
    def __init__(self):
        self._productos = []

    def agregar(self, producto):
        if producto not in CATALOGO:
            raise ValueError(f"Producto no existe en el catálogo: {producto}")
        if producto in self._productos:
            raise ValueError(f"El producto ya está en el carrito: {producto}")
        self._productos.append(producto)

    def quitar(self, producto):
        if producto not in self._productos:
            raise ValueError(f"El producto no está en el carrito: {producto}")
        self._productos.remove(producto)

    def cantidad(self):
        return len(self._productos)

    def productos(self):
        return list(self._productos)

    def subtotal(self):
        return sum((CATALOGO[p] for p in self._productos), Decimal("0.00"))
