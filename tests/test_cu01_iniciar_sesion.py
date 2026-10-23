"""CU-01 · Iniciar sesión — EJEMPLO RESUELTO entregado por el docente (no cuenta como aporte)."""
import pytest
from auth import (iniciar_sesion, MSG_USUARIO_REQUERIDO, MSG_CLAVE_REQUERIDA,
                  MSG_NO_COINCIDE, MSG_BLOQUEADO)


# Partición de equivalencia: clase válida (RN-A1)
@pytest.mark.parametrize("usuario", ["standard_user", "problem_user", "performance_glitch_user",
                                     "error_user", "visual_user"])
def test_cu01_usuario_valido_accede(usuario):
    assert iniciar_sesion(usuario, "secret_sauce") == (True, "")


# Partición de equivalencia: campos vacíos (RN-A2, RN-A3)
@pytest.mark.parametrize("usuario, clave, mensaje", [
    ("", "secret_sauce", MSG_USUARIO_REQUERIDO),
    (None, "secret_sauce", MSG_USUARIO_REQUERIDO),
    ("standard_user", "", MSG_CLAVE_REQUERIDA),
    ("standard_user", None, MSG_CLAVE_REQUERIDA),
], ids=["usuario_vacio", "usuario_none", "clave_vacia", "clave_none"])
def test_cu01_campo_vacio_devuelve_mensaje_de_requerido(usuario, clave, mensaje):
    assert iniciar_sesion(usuario, clave) == (False, mensaje)


# Tabla de decisión: credenciales que no coinciden (RN-A1: distingue mayúsculas, no recorta espacios)
@pytest.mark.parametrize("usuario, clave", [
    ("Standard_User", "secret_sauce"),
    (" standard_user", "secret_sauce"),
], ids=["mayusculas", "espacio_inicial"])
def test_cu01_credenciales_incorrectas_son_rechazadas(usuario, clave):
    assert iniciar_sesion(usuario, clave) == (False, MSG_NO_COINCIDE)


# Tabla de decisión: usuario bloqueado (RN-A2)
def test_cu01_usuario_bloqueado_no_accede():
    assert iniciar_sesion("locked_out_user", "secret_sauce") == (False, MSG_BLOQUEADO)
