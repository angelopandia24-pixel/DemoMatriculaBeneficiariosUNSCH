import pytest
from decimal import Decimal
from dominio.politica import PoliticaMatricula
from dominio.excepciones import InvalidPolicyError
from Aplicacion.calculadora import CalculadoraMatricula
from dominio.reglasNegocio import RecargoExtemporaneo

def test_no_permite_reglas_duplicadas():
    with pytest.raises(InvalidPolicyError):
        PoliticaMatricula("bad", Decimal("60"), ("beca", "beca"))

def test_no_permite_reglas_no_registradas():
    calc = CalculadoraMatricula([RecargoExtemporaneo()])
    politica = PoliticaMatricula("bad", Decimal("60"), ("regla_inventada",))
    from datetime import date
    from dominio.entidades import Estudiante, Matricula
    m = Matricula(Estudiante("A1", "Prueba", False, False), "2026-II",
                  date(2026, 8, 1), date(2026, 8, 2))
    with pytest.raises(InvalidPolicyError):
        calc.calcular(m, politica)
