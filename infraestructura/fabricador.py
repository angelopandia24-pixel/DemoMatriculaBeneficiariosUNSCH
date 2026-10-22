from datetime import date
from dominio.entidades import Estudiante, Matricula

class MatriculaFactory:
    @staticmethod
    def crear(
        codigo: str, 
        nombre: str, 
        es_extemporaneo: bool = False, 
        desaprobado: bool = False, 
        becario: bool = False, 
        semestre: str = "2026-II", 
        fecha_limite: date = date(2026, 8, 15)
    ) -> Matricula:
        
        estudiante = Estudiante(
            codigo=codigo,
            nombre_completo=nombre,
            indice_desaprobatorio=desaprobado,
            beneficiario_beca_violencia=becario
        )
        
        # Determina la fecha de matrícula según si es extemporánea o no
        fecha_pago = date(2026, 8, 20) if es_extemporaneo else date(2026, 8, 10)
        
        return Matricula(
            estudiante=estudiante,
            semestre=semestre,
            fecha_matricula=fecha_pago,
            fecha_limite=fecha_limite
        )