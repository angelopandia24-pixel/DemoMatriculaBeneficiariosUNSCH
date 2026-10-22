from dataclasses import dataclass
from decimal import Decimal
from dominio.entidades import Matricula
from dominio.reglasNegocio import ReglaMatricula, EjecucionRegla
from dominio.politica import PoliticaMatricula
from dominio.moneda import dinero
from dominio.excepciones import InvalidPolicyError

@dataclass(frozen=True, slots=True)
class Liquidacion:
    codigo_estudiante: str
    nombre_estudiante: str
    semestre: str
    version_politica: str
    importe_base: Decimal
    ejecuciones: tuple[EjecucionRegla, ...]
    importe_final: Decimal


class CalculadoraMatricula:
    def __init__(self, reglas: list[ReglaMatricula]):
        self._reglas = {regla.regla_id: regla for regla in reglas}
        if len(self._reglas) != len(reglas):
            raise InvalidPolicyError("Regla duplicada.")

    def calcular(self, matricula: Matricula, politica: PoliticaMatricula) -> Liquidacion:
        desconocidas = set(politica.orden_reglas) - set(self._reglas)
        if desconocidas:
            raise InvalidPolicyError(f"Reglas no registradas: {sorted(desconocidas)}")
        monto = dinero(politica.costo_base)
        base = monto
        historial = []
        for regla_id in politica.orden_reglas:
            resultado = self._reglas[regla_id].evaluar(monto, matricula)
            historial.append(resultado)
            monto = resultado.despues
        return Liquidacion(
            codigo_estudiante=matricula.estudiante.codigo,
            nombre_estudiante=matricula.estudiante.nombre_completo,
            semestre=matricula.semestre,
            version_politica=politica.version,
            importe_base=base,
            ejecuciones=tuple(historial),
            importe_final=dinero(monto),
        )
