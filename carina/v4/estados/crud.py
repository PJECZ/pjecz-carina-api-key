"""
Estados v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.estados.models import Estado


def get_estados(database: Session) -> Any:
    """Consultar los estados"""
    return database.query(Estado).filter_by(estatus="A").order_by(Estado.clave)


def get_estado(database: Session, estado_id: int) -> Estado:
    """Consultar un estado por su id"""
    estado = database.query(Estado).get(estado_id)
    if estado is None:
        raise MyNotExistsError("No existe ese estado")
    if estado.estatus != "A":
        raise MyIsDeletedError("No es activo ese estado, está eliminado")
    return estado


def get_estado_with_clave(database: Session, estado_clave: str) -> Estado:
    """Consultar un estado por su clave"""
    try:
        clave = safe_clave(estado_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    try:
        estado = database.query(Estado).filter_by(clave=clave).one()
    except NoResultFound:
        raise MyNotExistsError("No existe ese estado")
    if estado.estatus != "A":
        raise MyIsDeletedError("No es activo ese estado, está eliminado")
    return estado
