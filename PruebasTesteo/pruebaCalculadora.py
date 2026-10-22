from datetime import date
from decimal import Decimal
from Aplicacion.calculadora import CalculadoraMatricula
from dominio.entidades import Estudiante, Matricula
from dominio.politica import PoliticaMatricula
from dominio.reglasNegocio import RecargoExtemporaneo, RecargoIndiceDesaprobatorio, AplicarBecaViolenciaSociopolitica

def setup():
    estudiante = Estudiante("X002", "Caso completo", True, True)
    matricula = Matricula(estudiante, "2026-II", date(2026, 8, 20), date(2026, 8, 15))
    calculadora = CalculadoraMatricula([
        RecargoExtemporaneo(),
        RecargoIndiceDesaprobatorio(),
        AplicarBecaViolenciaSociopolitica()
    ])
    return matricula, calculadora

def test_recargos_antes_de_beca_dan_45_soles():
    matricula, calc = setup()
    politica = PoliticaMatricula("test-01", Decimal("60"), ("extemporanea", "desaprobatorio", "beca"))
    assert calc.calcular(matricula, politica).importe_final == Decimal("45.00")

def test_beca_antes_de_recargos_da_60_soles():
    matricula, calc = setup()
    politica = PoliticaMatricula("test-02", Decimal("60"), ("beca", "desaprobatorio", "extemporanea"))
    assert calc.calcular(matricula, politica).importe_final == Decimal("60.00")

def test_liquidacion_guarda_trazabilidad_de_todas_las_reglas():
    matricula, calc = setup()
    politica = PoliticaMatricula("test-03", Decimal("60"), ("extemporanea", "desaprobatorio", "beca"))
    resultado = calc.calcular(matricula, politica)
    assert len(resultado.ejecuciones) == 3
    assert resultado.version_politica == "test-03"
    assert resultado.ejecuciones[0].antes == Decimal("60.00")
    assert resultado.ejecuciones[-1].despues == Decimal("45.00")
