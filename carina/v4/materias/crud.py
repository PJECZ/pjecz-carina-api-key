"""
Materias v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.materias.models import Materia


def get_materias(database: Session) -> Any:
    """Consultar las materias activas"""
    return database.query(Materia).filter_by(estatus="A").order_by(Materia.clave)


def get_materia(database: Session, materia_id: int) -> Materia:
    """Consultar una materia por su id"""
    materia = database.query(Materia).get(materia_id)
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia, está eliminado")
    return materia


def get_materia_with_clave(database: Session, materia_clave: str) -> Materia:
    """Consultar una materia por su clave"""
    try:
        clave = safe_clave(materia_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    materia = database.query(Materia).filter_by(clave=clave).first()
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia, está eliminado")
    return materia
