"""
Exh Externos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_externos.models import ExhExterno
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave


def get_exh_externos(database: Session) -> Any:
    """Consultar los externos activos"""
    return database.query(ExhExterno).filter_by(estatus="A").order_by(ExhExterno.clave)


def get_exh_externo(database: Session, exh_externo_id: int) -> ExhExterno:
    """Consultar un externo por su id"""
    exh_externo = database.query(ExhExterno).get(exh_externo_id)
    if exh_externo is None:
        raise MyNotExistsError("No existe ese externo")
    if exh_externo.estatus != "A":
        raise MyIsDeletedError("No es activo ese externo, está eliminado")
    return exh_externo


def get_exh_externo_with_clave(database: Session, exh_externo_clave: str) -> ExhExterno:
    """Consultar un externo por su clave"""
    try:
        exh_externo_clave = safe_clave(exh_externo_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    exh_externo = database.query(ExhExterno).filter_by(clave=exh_externo_clave).first()
    if exh_externo is None:
        raise MyNotExistsError("No existe ese externo")
    if exh_externo.estatus != "A":
        raise MyIsDeletedError("No es activo ese externo, está eliminado")
    return exh_externo
