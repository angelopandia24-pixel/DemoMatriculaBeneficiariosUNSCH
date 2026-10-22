from pathlib import Path
from Aplicacion.calculadora import CalculadoraMatricula
from dominio.reglasNegocio import (RecargoExtemporaneo,RecargoIndiceDesaprobatorio, AplicarBecaViolenciaSociopolitica,)
from infraestructura.politicaJson import RepositorioPoliticasJSON
from dominio.politica import PoliticaMatricula
from infraestructura.fabricador import MatriculaFactory
ROOT = Path(__file__).resolve().parents[1]

def mostrar_liquidacion(liquidacion):
    print("\\n" + "=" * 66)
    print(f"LIQUIDACIÓN DE MATRÍCULA: {liquidacion.semestre}")
    print(f"Estudiante: {liquidacion.nombre_estudiante} ({liquidacion.codigo_estudiante})")
    print(f"Política aplicada: {liquidacion.version_politica}")
    print(f"Importe base: S/ {liquidacion.importe_base:.2f}")
    print("-" * 66)
    for paso, ejecucion in enumerate(liquidacion.ejecuciones, start=1):
        estado = "APLICADA" if ejecucion.aplicada else "NO APLICADA"
        print(f"{paso}. {ejecucion.descripcion}: {estado}")
        print(f"   S/ {ejecucion.antes:.2f} -> S/ {ejecucion.despues:.2f}")
        print(f"   Motivo: {ejecucion.motivo}")
    print("-" * 66)
    print(f"TOTAL A PAGAR: S/ {liquidacion.importe_final:.2f}")
    print("=" * 66)

def main():
    repositorio = RepositorioPoliticasJSON()
    calculadora = CalculadoraMatricula([
        RecargoExtemporaneo(),
        RecargoIndiceDesaprobatorio(),
        AplicarBecaViolenciaSociopolitica(),
    ])

    angelo = MatriculaFactory.crear(
        codigo="27230001",
        nombre="Pandia Cáceres, Angelo",
        es_extemporaneo=True,
        desaprobado=True,
        becario=True
    )
    andre = MatriculaFactory.crear(
        codigo="27220002",
        nombre="Apaico Paucar, Andre",
        es_extemporaneo=True,
        desaprobado=True,
        becario=True
    )

    carlos = MatriculaFactory.crear(
        codigo="27240003",
        nombre="García Mendoza, Carlos"
    )

    politica_1 = repositorio.cargar(ROOT / "politicasCosteBase" / "unsch_2026_ii.json")
    politica_2 = PoliticaMatricula(version="UNSCH-2026-II-DEMO-02", costo_base="60.00", orden_reglas=("beca", "desaprobatorio", "extemporanea"),)

    mostrar_liquidacion(calculadora.calcular(angelo, politica_1))
    mostrar_liquidacion(calculadora.calcular(andre, politica_2))
    mostrar_liquidacion(calculadora.calcular(carlos, politica_1))
if __name__ == "__main__":
    main()
