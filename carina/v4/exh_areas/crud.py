"""
Exh Areas v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_areas.models import ExhArea
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave


def get_exh_areas(database: Session) -> Any:
    """Consultar los áreas"""
    return database.query(ExhArea).filter_by(estatus="A").order_by(ExhArea.clave)


def get_exh_area(database: Session, exh_area_id: int) -> ExhArea:
    """Consultar un área por su id"""
    exh_area = database.query(ExhArea).get(exh_area_id)
    if exh_area is None:
        raise MyNotExistsError("No existe ese area")
    if exh_area.estatus != "A":
        raise MyIsDeletedError("No es activo ese area, está eliminado")
    return exh_area


def get_exh_area_with_clave(database: Session, exh_area_clave: str) -> ExhArea:
    """Consultar un area por su clave"""
    try:
        clave = safe_clave(exh_area_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    exh_area = database.query(ExhArea).filter_by(clave=clave).first()
    if exh_area is None:
        raise MyNotExistsError("No existe ese area")
    if exh_area.estatus != "A":
        raise MyIsDeletedError("No es activo ese area, está eliminado")
    return exh_area
