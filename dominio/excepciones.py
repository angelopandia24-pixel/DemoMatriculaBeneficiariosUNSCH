class DomainError(Exception):
    """Error base del dominio de matrícula."""

class InvalidPolicyError(DomainError):
    """La política contiene reglas desconocidas, duplicadas o datos inválidos."""

class InvalidEnrollmentError(DomainError):
    """La matrícula contiene datos incompatibles con las reglas del dominio."""
