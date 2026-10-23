# Pruebas unitarias · Caso de estudio A — Swag Labs

**Asignatura:** TI3-312 Aseguramiento de la Calidad del Software (UNIBE)
**Estudiante:** Bryan José Peguero Camilo · 25-1585
**Docente:** Lorenzo Martínez
**Actividad:** Actividad 6 — Diseño e implementación de pruebas unitarias

Pruebas con **pytest** para los casos de uso **CU-02 (carrito)**, **CU-03 (datos de envío)** y **CU-04 (resumen del pedido)** del caso de estudio Swag Labs. CU-01 es el ejemplo resuelto y no cuenta como aporte.

> **Nota sobre `src/`:** el archivo `TI3312_S6_Casos_de_Estudio_Codigo.zip` no estaba disponible en Blackboard al momento de la entrega, por lo que los módulos de `src/` se escribieron siguiendo exactamente la ficha del caso de estudio A (RN-A1 a RN-A6). Si se reemplazan por los módulos oficiales, las pruebas se ejecutan igual con `pytest -v`; cualquier fallo sería un hallazgo del módulo frente a la ficha.

## Requisitos

- Python 3.10 o superior
- Git

## Cómo ejecutar las pruebas

```bash
git clone https://github.com/lulon13/pruebas-unitarias.git
cd pruebas-unitarias

python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate

pip install -r requirements.txt
pytest -v
```

Resultado esperado: **46 passed** (12 del ejemplo resuelto CU-01 + 34 propias de CU-02, CU-03 y CU-04).

Para ejecutar solo un caso de uso:

```bash
pytest -v tests/test_cu02_carrito.py
pytest -v tests/test_cu03_datos_envio.py
pytest -v tests/test_cu04_resumen.py
```

> Ejecute `pytest` desde esta carpeta (donde está `pytest.ini`); si no, aparecerá `ModuleNotFoundError`.

## Estructura

```
pruebas-unitarias/
├── README.md            este archivo
├── requirements.txt
├── pytest.ini
├── src/                 módulos del caso de estudio (según la ficha)
│   ├── auth.py          CU-01 iniciar_sesion
│   ├── carrito.py       CU-02 clase Carrito
│   └── checkout.py      CU-03 validar_datos_envio · CU-04 calcular_resumen
├── tests/
│   ├── test_cu01_iniciar_sesion.py   ejemplo resuelto (docente)
│   ├── test_cu02_carrito.py          aporte
│   ├── test_cu03_datos_envio.py      aporte
│   └── test_cu04_resumen.py          aporte
└── docs/
    └── DOCUMENTACION.md  propósito de cada prueba, técnica, regla y hallazgos
```

La documentación completa está en [docs/DOCUMENTACION.md](docs/DOCUMENTACION.md).
