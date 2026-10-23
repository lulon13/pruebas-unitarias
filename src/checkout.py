"""CU-03 · Capturar datos de envío (RN-A5) y CU-04 · Calcular el resumen (RN-A6)."""
from decimal import Decimal, ROUND_HALF_UP

ERR_NOMBRE = "Error: First Name is required"
ERR_APELLIDO = "Error: Last Name is required"
ERR_POSTAL = "Error: Postal Code is required"

TASA_IMPUESTO = Decimal("0.08")
CENTAVO = Decimal("0.01")


def _vacio(valor):
    return valor is None or str(valor).strip() == ""


def validar_datos_envio(nombre, apellido, codigo_postal):
    """Devuelve "" si todo es válido o el primer error en el orden nombre, apellido, código postal."""
    if _vacio(nombre):
        return ERR_NOMBRE
    if _vacio(apellido):
        return ERR_APELLIDO
    if _vacio(codigo_postal):
        return ERR_POSTAL
    return ""


def calcular_resumen(subtotal):
    """Devuelve {"subtotal", "impuesto", "total"} como Decimal. Impuesto 8 % redondeado al centavo."""
    subtotal = Decimal(str(subtotal))
    if subtotal < 0:
        raise ValueError("El subtotal no puede ser negativo")
    impuesto = (subtotal * TASA_IMPUESTO).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    subtotal = subtotal.quantize(CENTAVO, rounding=ROUND_HALF_UP)
    return {"subtotal": subtotal, "impuesto": impuesto, "total": subtotal + impuesto}
