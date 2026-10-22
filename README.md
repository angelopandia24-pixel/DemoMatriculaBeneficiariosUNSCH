# Motor configurable de matrícula UNSCH

Prototipo académico en Python para modelar el cálculo de matrícula 2026-II con reglas ordenables, polimorfismo y trazabilidad.

## Requisitos
- Python 3.11 o superior
- pytest para ejecutar pruebas

## Ejecutar
Desde la carpeta del proyecto:

```bash
python -m presentation.main
```

## Pruebas (TDD)
Instalar herramientas de desarrollo y ejecutar:

```bash
python -m pip install -e ".[dev]"
pytest -v
```

## Cambiar el orden de las reglas
Editar `policies/unsch_2026_ii.json`, especialmente `orden_reglas`. Valores válidos:
- `extemporanea`
- `desaprobatorio`
- `beca`

El orden es una decisión de política institucional, no una consecuencia accidental del MRO.

## Alcance
Es una demostración académica con estudiantes, fechas y políticas ficticias. No integra el sistema real de la UNSCH ni sustituye la validación legal/administrativa de los cobros.
