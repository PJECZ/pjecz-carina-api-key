"""
Materias v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from carina.core.materias.models import Materia
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave


def get_materias(database: Session) -> Any:
    """Consultar las materias"""
    return database.query(Materia).filter_by(estatus="A").filter_by(en_exh_exhortos=True).order_by(Materia.clave)


def get_materia(database: Session, materia_id: int) -> Materia:
    """Consultar una materia por su id"""
    materia = database.query(Materia).get(materia_id)
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activa esa materia, está eliminada")
    if materia.en_exh_exhortos is False:
        raise MyNotExistsError("No se usa esa materia en exhortos electrónicos")
    return materia


def get_materia_with_clave(database: Session, materia_clave: str) -> Materia:
    """Consultar una materia por su clave"""
    try:
        clave = safe_clave(materia_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    try:
        materia = database.query(Materia).filter_by(clave=clave).one()
    except NoResultFound:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia, está eliminado")
    if materia.en_exh_exhortos is False:
        raise MyNotExistsError("No se usa esa materia en exhortos electrónicos")
    return materia
