import json
from pathlib import Path
from dominio.politica import PoliticaMatricula
from dominio.excepciones import InvalidPolicyError

class RepositorioPoliticasJSON:
    """Adaptador de infraestructura: convierte un JSON en una política del dominio."""
    def cargar(self, ruta: str | Path) -> PoliticaMatricula:
        try:
            datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
            return PoliticaMatricula(
                version=datos["version"],
                costo_base=datos["costo_base"],
                orden_reglas=tuple(datos["orden_reglas"]),
            )
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, InvalidPolicyError):
                raise
            raise InvalidPolicyError(f"No se pudo cargar la política: {exc}") from exc
