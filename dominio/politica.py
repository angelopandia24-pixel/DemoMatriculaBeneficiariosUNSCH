from dataclasses import dataclass
from decimal import Decimal
from .moneda import dinero
from .excepciones import InvalidPolicyError

@dataclass(frozen=True, slots=True)
class PoliticaMatricula:
    version: str
    costo_base: Decimal
    orden_reglas: tuple[str, ...]

    def __post_init__(self):
        object.__setattr__(self, "costo_base", dinero(self.costo_base))
        if not self.version.strip():
            raise InvalidPolicyError("La política debe tener una versión.")
        if len(self.orden_reglas) != len(set(self.orden_reglas)):
            raise InvalidPolicyError("La política no puede repetir reglas.")
        if not self.orden_reglas:
            raise InvalidPolicyError("La política debe declarar al menos una regla.")
