from dataclasses import dataclass
from datetime import date
from .excepciones import InvalidEnrollmentError

@dataclass(frozen=True, slots=True)
class Estudiante:
    codigo: str
    nombre_completo: str
    indice_desaprobatorio: bool
    beneficiario_beca_violencia: bool

    def __post_init__(self):
        if not self.codigo.strip():
            raise ValueError("El código universitario no puede estar vacío.")
        if not self.nombre_completo.strip():
            raise ValueError("El nombre del estudiante no puede estar vacío.")


@dataclass(frozen=True, slots=True)
class Matricula:
    estudiante: Estudiante
    semestre: str
    fecha_matricula: date
    fecha_limite: date

    def __post_init__(self):
        if not self.semestre.strip():
            raise InvalidEnrollmentError("El semestre es obligatorio.")
    @property
    def es_extemporanea(self) -> bool:
        return self.fecha_matricula > self.fecha_limite
