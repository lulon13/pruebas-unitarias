"""CU-04 · Calcular el resumen del pedido (RN-A6). Resultados esperados derivados de la ficha."""
from decimal import Decimal

import pytest
from checkout import calcular_resumen


# Partición de equivalencia: subtotal positivo típico (Backpack + Bike Light)
def test_cu04_resumen_de_compra_tipica():
    r = calcular_resumen(Decimal("39.98"))
    assert r == {"subtotal": Decimal("39.98"), "impuesto": Decimal("3.20"),
                 "total": Decimal("43.18")}


# Los importes deben ser Decimal (no float) para evitar errores de céntimos
def test_cu04_los_importes_son_decimal():
    r = calcular_resumen(Decimal("39.98"))
    assert all(isinstance(v, Decimal) for v in r.values())


# Valor límite inferior: subtotal 0 es válido
def test_cu04_subtotal_cero_es_valido():
    assert calcular_resumen(Decimal("0")) == {"subtotal": Decimal("0.00"),
                                               "impuesto": Decimal("0.00"),
                                               "total": Decimal("0.00")}


# Valor límite: justo debajo de 0 → error
@pytest.mark.parametrize("subtotal", [Decimal("-0.01"), Decimal("-29.99")],
                         ids=["-0.01", "-29.99"])
def test_cu04_subtotal_negativo_lanza_value_error(subtotal):
    with pytest.raises(ValueError):
        calcular_resumen(subtotal)


# Valores límite del redondeo al centavo (mitad hacia arriba)
@pytest.mark.parametrize("subtotal, impuesto", [
    (Decimal("0.0625"), Decimal("0.01")),   # 0.005  → exactamente la mitad, sube
    (Decimal("0.0624"), Decimal("0.00")),   # 0.004992 → baja
    (Decimal("9.99"),   Decimal("0.80")),   # 0.7992 → 0.80
    (Decimal("7.99"),   Decimal("0.64")),   # 0.6392 → 0.64
], ids=["mitad_sube", "debajo_baja", "9.99", "7.99"])
def test_cu04_impuesto_redondea_al_centavo_mitad_hacia_arriba(subtotal, impuesto):
    assert calcular_resumen(subtotal)["impuesto"] == impuesto


# Valor límite superior práctico: los 6 productos del catálogo (129.94)
def test_cu04_total_con_carrito_lleno():
    r = calcular_resumen(Decimal("129.94"))
    assert r["impuesto"] == Decimal("10.40")   # 10.3952 → 10.40
    assert r["total"] == Decimal("140.34")
