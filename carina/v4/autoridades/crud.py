"""
Autoridades v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.autoridades.models import Autoridad
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_autoridades(
    database: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    es_extinto: bool = None,
) -> Any:
    """Consultar los autoridades activos"""
    consulta = database.query(Autoridad)
    if distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if es_extinto is not None:
        consulta = consulta.filter_by(es_extinto=es_extinto)
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave)


def get_autoridad(database: Session, autoridad_id: int) -> Autoridad:
    """Consultar un autoridad por su id"""
    autoridad = database.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad


def get_autoridad_with_clave(database: Session, autoridad_clave: str) -> Autoridad:
    """Consultar un autoridad por su clave"""
    try:
        clave = safe_clave(autoridad_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    autoridad = database.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad
