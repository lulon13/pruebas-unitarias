"""CU-01 · Iniciar sesión (RN-A1 a RN-A3)."""

USUARIOS_VALIDOS = {
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
}
CLAVE = "secret_sauce"
USUARIO_BLOQUEADO = "locked_out_user"

MSG_USUARIO_REQUERIDO = "Epic sadface: Username is required"
MSG_CLAVE_REQUERIDA = "Epic sadface: Password is required"
MSG_NO_COINCIDE = "Epic sadface: Username and password do not match any user in this service"
MSG_BLOQUEADO = "Epic sadface: Sorry, this user has been locked out."


def iniciar_sesion(usuario, clave):
    """Devuelve (True, "") si el acceso es válido o (False, mensaje) con el primer problema."""
    if not usuario:
        return False, MSG_USUARIO_REQUERIDO
    if not clave:
        return False, MSG_CLAVE_REQUERIDA
    if usuario not in USUARIOS_VALIDOS or clave != CLAVE:
        return False, MSG_NO_COINCIDE
    if usuario == USUARIO_BLOQUEADO:
        return False, MSG_BLOQUEADO
    return True, ""
