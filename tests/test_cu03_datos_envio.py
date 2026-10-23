"""CU-03 · Capturar datos de envío (RN-A5). Resultados esperados derivados de la ficha."""
import pytest
from checkout import validar_datos_envio

ERR_NOMBRE = "Error: First Name is required"
ERR_APELLIDO = "Error: Last Name is required"
ERR_POSTAL = "Error: Postal Code is required"


# Tabla de decisión — regla R1: los tres datos presentes
def test_cu03_datos_completos_no_devuelven_error():
    assert validar_datos_envio("Ana", "Prueba", "10101") == ""


# Valor límite: un solo carácter por campo es suficiente
def test_cu03_un_caracter_por_campo_es_valido():
    assert validar_datos_envio("A", "B", "1") == ""


# Tabla de decisión completa (V = presente, F = vacío): se informa el PRIMER error en orden
@pytest.mark.parametrize("nombre, apellido, postal, esperado", [
    ("Ana", "Prueba", "",      ERR_POSTAL),    # R2: V V F
    ("Ana", "",       "10101", ERR_APELLIDO),  # R3: V F V
    ("Ana", "",       "",      ERR_APELLIDO),  # R4: V F F
    ("",    "Prueba", "10101", ERR_NOMBRE),    # R5: F V V
    ("",    "Prueba", "",      ERR_NOMBRE),    # R6: F V F
    ("",    "",       "10101", ERR_NOMBRE),    # R7: F F V
    ("",    "",       "",      ERR_NOMBRE),    # R8: F F F
], ids=["R2", "R3", "R4", "R5", "R6", "R7", "R8"])
def test_cu03_tabla_de_decision_informa_el_primer_error(nombre, apellido, postal, esperado):
    assert validar_datos_envio(nombre, apellido, postal) == esperado


# Partición de equivalencia: "solo espacios" pertenece a la clase VACÍO
@pytest.mark.parametrize("nombre, apellido, postal, esperado", [
    ("   ", "Prueba", "10101", ERR_NOMBRE),
    ("Ana", "\t",     "10101", ERR_APELLIDO),
    ("Ana", "Prueba", "  ",    ERR_POSTAL),
], ids=["nombre", "apellido", "codigo_postal"])
def test_cu03_solo_espacios_cuenta_como_vacio(nombre, apellido, postal, esperado):
    assert validar_datos_envio(nombre, apellido, postal) == esperado


# Partición de equivalencia: None también es un dato ausente
def test_cu03_valor_none_cuenta_como_vacio():
    assert validar_datos_envio("Ana", "Prueba", None) == ERR_POSTAL
