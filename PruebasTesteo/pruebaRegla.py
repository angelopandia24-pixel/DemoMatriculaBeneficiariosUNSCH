from datetime import date
from decimal import Decimal
from dominio.entidades import Estudiante, Matricula
from dominio.reglasNegocio import (
    RecargoExtemporaneo,
    RecargoIndiceDesaprobatorio,
    AplicarBecaViolenciaSociopolitica,
)

def crear_matricula(tarde=True, desaprobado=True, beca=True):
    estudiante = Estudiante("X001", "Estudiante de prueba", desaprobado, beca)
    return Matricula(estudiante, "2026-II",
                     date(2026, 8, 20) if tarde else date(2026, 8, 10),
                     date(2026, 8, 15))

def test_recargo_extemporaneo_se_aplica_si_llega_tarde():
    r = RecargoExtemporaneo().evaluar(Decimal("60.00"), crear_matricula(tarde=True))
    assert r.aplicada is True
    assert r.despues == Decimal("75.00")

def test_recargo_extemporaneo_no_se_aplica_en_plazo():
    r = RecargoExtemporaneo().evaluar(Decimal("60.00"), crear_matricula(tarde=False))
    assert r.aplicada is False
    assert r.despues == Decimal("60.00")

def test_recargo_academico():
    r = RecargoIndiceDesaprobatorio().evaluar(Decimal("60.00"), crear_matricula())
    assert r.despues == Decimal("75.00")

def test_beca_reduce_a_la_mitad_el_importe_acumulado():
    r = AplicarBecaViolenciaSociopolitica().evaluar(Decimal("90.00"), crear_matricula())
    assert r.despues == Decimal("45.00")
