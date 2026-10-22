from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from .entidades import Matricula
from .moneda import dinero

@dataclass(frozen=True, slots=True)
class EjecucionRegla:
    regla_id: str
    descripcion: str
    aplicada: bool
    antes: Decimal
    despues: Decimal
    motivo: str


class ReglaMatricula(ABC):
    regla_id: str
    descripcion: str

    @abstractmethod
    def evaluar(self, monto: Decimal, matricula: Matricula) -> EjecucionRegla:
        raise NotImplementedError

class RecargoExtemporaneo(ReglaMatricula):
    regla_id = "extemporanea"
    descripcion = "Recargo por matrícula fuera de fecha"

    def evaluar(self, monto: Decimal, matricula: Matricula) -> EjecucionRegla:
        aplicada = matricula.es_extemporanea
        despues = dinero(monto + Decimal("15.00")) if aplicada else monto
        motivo = "Matrícula posterior a la fecha límite." if aplicada else "Matrícula dentro del plazo."
        return EjecucionRegla(self.regla_id, self.descripcion, aplicada, monto, despues, motivo)

class RecargoIndiceDesaprobatorio(ReglaMatricula):
    regla_id = "desaprobatorio"
    descripcion = "Recargo por índice académico desaprobatorio"

    def evaluar(self, monto: Decimal, matricula: Matricula) -> EjecucionRegla:
        aplicada = matricula.estudiante.indice_desaprobatorio
        despues = dinero(monto + Decimal("15.00")) if aplicada else monto
        motivo = "Presenta índice desaprobatorio." if aplicada else "No presenta índice desaprobatorio."
        return EjecucionRegla(self.regla_id, self.descripcion, aplicada, monto, despues, motivo)

class AplicarBecaViolenciaSociopolitica(ReglaMatricula):
    regla_id = "beca"
    descripcion = "Reducción del 50 % por beca para afectados por violencia sociopolítica"

    def evaluar(self, monto: Decimal, matricula: Matricula) -> EjecucionRegla:
        aplicada = matricula.estudiante.beneficiario_beca_violencia
        despues = dinero(monto / Decimal("2")) if aplicada else monto
        motivo = "Beneficiario de la beca: se reduce a la mitad el importe acumulado." if aplicada else "No es beneficiario de esta beca."
        return EjecucionRegla(self.regla_id, self.descripcion, aplicada, monto, despues, motivo)
