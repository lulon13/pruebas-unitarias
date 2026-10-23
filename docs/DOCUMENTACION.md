# Pruebas unitarias · Caso de estudio A — Swag Labs

**Autor:** Bryan José Peguero Camilo (25-1585)   **Fecha:** 23/10/2026
**Asignatura:** TI3-312 Aseguramiento de la Calidad del Software — UNIBE

## Casos de uso cubiertos

- **CU-02 Gestionar el carrito** — regla RN-A4 (`src/carrito.py`, clase `Carrito`)
- **CU-03 Capturar datos de envío** — regla RN-A5 (`src/checkout.py`, `validar_datos_envio`)
- **CU-04 Calcular el resumen del pedido** — regla RN-A6 (`src/checkout.py`, `calcular_resumen`)

CU-01 (iniciar sesión) es el ejemplo resuelto; se conserva en `tests/` solo como referencia.

## Cómo se diseñaron

Cada resultado esperado se tomó de la ficha del caso de estudio, no del código. Se aplicaron las técnicas del laboratorio 3:

- **Partición de equivalencia:** una clase válida y al menos una inválida por regla.
- **Valores límite:** el límite y sus vecinos (0 y −0.01; 1 carácter; redondeo en 0.005).
- **Tabla de decisión:** las 8 combinaciones de nombre / apellido / código postal.
- **Transición de estados:** carrito VACÍO ↔ CON_PRODUCTOS, incluidas las transiciones inválidas.

### Matriz de diseño

| Caso de uso | Regla | Técnica | Entrada | Resultado esperado |
|---|---|---|---|---|
| CU-02 | RN-A4 | Transición de estados | Carrito nuevo | 0 productos, subtotal 0.00 |
| CU-02 | RN-A4 | Partición (válida) | Agregar «Sauce Labs Backpack» | Queda 1 producto |
| CU-02 | RN-A4 | Partición (inválida) | «Sauce Labs Backpak», «sauce labs backpack», «» | ValueError, carrito sin cambios |
| CU-02 | RN-A4 | Transición de estados | Agregar Backpack dos veces | ValueError, sigue 1 producto |
| CU-02 | RN-A4 | Transición de estados | Quitar Backpack que está | 0 productos |
| CU-02 | RN-A4 | Transición inválida | Quitar Backpack que no está (carrito vacío / con otro) | ValueError |
| CU-02 | RN-A4 | Partición | Backpack + Bike Light | Subtotal 39.98 |
| CU-02 | RN-A4 | Valor límite | Los 6 productos | 6 productos, subtotal 129.94 |
| CU-03 | RN-A5 | Tabla de decisión R1 | Ana / Prueba / 10101 | "" (sin error) |
| CU-03 | RN-A5 | Valor límite | A / B / 1 | "" (sin error) |
| CU-03 | RN-A5 | Tabla de decisión R2–R8 | Combinaciones con campos vacíos | Primer error en orden nombre → apellido → código |
| CU-03 | RN-A5 | Partición | Solo espacios o tabulador en cada campo | Error del campo (cuenta como vacío) |
| CU-03 | RN-A5 | Partición | Código postal None | Error: Postal Code is required |
| CU-04 | RN-A6 | Partición | Subtotal 39.98 | Impuesto 3.20, total 43.18 |
| CU-04 | RN-A6 | Partición | Subtotal 39.98 | Los tres importes son Decimal |
| CU-04 | RN-A6 | Valor límite | Subtotal 0 | 0.00 / 0.00 / 0.00 |
| CU-04 | RN-A6 | Valor límite | −0.01 y −29.99 | ValueError |
| CU-04 | RN-A6 | Valor límite (redondeo) | 0.0625 / 0.0624 / 9.99 / 7.99 | 0.01 / 0.00 / 0.80 / 0.64 |
| CU-04 | RN-A6 | Valor límite | Subtotal 129.94 | Impuesto 10.40, total 140.34 |

## Descripción de las pruebas

| Prueba | Caso de uso | Regla | Técnica | Propósito | Resultado esperado |
|---|---|---|---|---|---|
| test_cu02_carrito_nuevo_esta_vacio | CU-02 | RN-A4 | Transición de estados | Verifica el estado inicial del carrito | cantidad 0, productos [], subtotal 0.00 |
| test_cu02_agregar_producto_del_catalogo_lo_incluye | CU-02 | RN-A4 | Partición (válida) | Verifica que un producto del catálogo se agrega | [Backpack], cantidad 1 |
| test_cu02_agregar_producto_fuera_del_catalogo_es_rechazado [3 casos] | CU-02 | RN-A4 | Partición (inválida) | Verifica que solo se aceptan productos del catálogo, con nombre exacto | ValueError y carrito vacío |
| test_cu02_agregar_producto_repetido_es_rechazado_y_no_se_duplica | CU-02 | RN-A4 | Transición de estados | Verifica que un producto está una sola vez | ValueError, cantidad 1 |
| test_cu02_quitar_producto_presente_lo_elimina | CU-02 | RN-A4 | Transición de estados | Verifica que quitar devuelve el carrito a vacío | cantidad 0, subtotal 0.00 |
| test_cu02_quitar_producto_ausente_es_rechazado [2 casos] | CU-02 | RN-A4 | Transición inválida | Verifica que solo se quita lo que está en el carrito | ValueError, sin cambios |
| test_cu02_subtotal_suma_los_precios_del_catalogo | CU-02 | RN-A4 | Partición | Verifica la suma con precios del catálogo | 39.98 |
| test_cu02_carrito_con_los_seis_productos | CU-02 | RN-A4 | Valor límite | Verifica el carrito lleno | 6 productos, 129.94 |
| test_cu03_datos_completos_no_devuelven_error | CU-03 | RN-A5 | Tabla de decisión (R1) | Verifica el camino feliz | "" |
| test_cu03_un_caracter_por_campo_es_valido | CU-03 | RN-A5 | Valor límite | Verifica el mínimo no vacío | "" |
| test_cu03_tabla_de_decision_informa_el_primer_error [R2–R8] | CU-03 | RN-A5 | Tabla de decisión | Verifica el orden de los errores en las 7 combinaciones con vacíos | Primer error según el orden |
| test_cu03_solo_espacios_cuenta_como_vacio [3 casos] | CU-03 | RN-A5 | Partición | Verifica que un valor con solo espacios es vacío | Error del campo |
| test_cu03_valor_none_cuenta_como_vacio | CU-03 | RN-A5 | Partición | Verifica que None se trata como ausente | Error: Postal Code is required |
| test_cu04_resumen_de_compra_tipica | CU-04 | RN-A6 | Partición | Verifica impuesto 8 % y total | 39.98 / 3.20 / 43.18 |
| test_cu04_los_importes_son_decimal | CU-04 | RN-A6 | Partición | Verifica el tipo Decimal | Todos Decimal |
| test_cu04_subtotal_cero_es_valido | CU-04 | RN-A6 | Valor límite | Verifica el límite inferior válido | 0.00 / 0.00 / 0.00 |
| test_cu04_subtotal_negativo_lanza_value_error [2 casos] | CU-04 | RN-A6 | Valor límite | Verifica que un subtotal negativo es un error | ValueError |
| test_cu04_impuesto_redondea_al_centavo_mitad_hacia_arriba [4 casos] | CU-04 | RN-A6 | Valor límite | Verifica el redondeo mitad hacia arriba | 0.01 / 0.00 / 0.80 / 0.64 |
| test_cu04_total_con_carrito_lleno | CU-04 | RN-A6 | Valor límite | Verifica el mayor subtotal posible del catálogo | 10.40 / 140.34 |

**Total:** 34 pruebas propias (CU-02: 11 · CU-03: 13 · CU-04: 10) + 12 del ejemplo resuelto = **46 passed**.

## Hallazgos

| Prueba | Qué esperaba la ficha | Qué hizo el módulo | Conclusión |
|---|---|---|---|
| — | — | — | Ninguna prueba falló: el módulo cumple la ficha en los casos probados. |

Diferencia con el sitio real (no es un fallo del módulo): en saucedemo.com un nombre formado solo por espacios **sí** se acepta (hallado en la Actividad Práctica, DEF-01), mientras que la ficha (RN-A5) y el módulo lo tratan como vacío. La ficha prevalece.

## Instrucciones de ejecución

Ver [README.md](../README.md): `pip install -r requirements.txt` y `pytest -v` desde la carpeta `pruebas-unitarias`.

## Declaración de uso de IA

Se usó IA generativa (Claude, de Anthropic) como apoyo para proponer casos de prueba, redactar el código de las pruebas y esta documentación. Como el archivo con los módulos oficiales no estaba publicado, los módulos de `src/` también se redactaron con apoyo de IA a partir de la ficha. Cada resultado esperado se verificó contra la ficha del caso de estudio (RN-A4, RN-A5 y RN-A6), no contra el código del módulo, y todas las pruebas se ejecutaron con `pytest -v`.
