"""
Municipios v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.estados.models import Estado
from ...core.municipios.models import Municipio
from ..estados.crud import get_estado_with_clave


def get_municipios(database: Session, estado_clave: str = None) -> Any:
    """Consultar los municipios"""
    try:
        estado_clave = safe_clave(estado_clave).zfill(2)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    consulta = database.query(Municipio)
    if estado_clave is not None:
        estado = get_estado_with_clave(database, estado_clave)
        consulta = consulta.filter_by(estado_id=estado.id)
    return consulta.filter_by(estatus="A").order_by(Municipio.clave)


def get_municipio(database: Session, municipio_id: int) -> Municipio:
    """Consultar un municipio por su id"""
    municipio = database.query(Municipio).get(municipio_id)
    if municipio is None:
        raise MyNotExistsError("No existe ese municipio")
    if municipio.estatus != "A":
        raise MyIsDeletedError("No es activo ese municipio, está eliminado")
    return municipio


def get_municipio_with_clave(database: Session, estado_clave: str, municipio_clave: str) -> Municipio:
    """Consultar un municipio por su clave y la clave de su estado"""
    try:
        estado_clave = safe_clave(estado_clave).zfill(2)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    try:
        municipio_clave = safe_clave(municipio_clave).zfill(3)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    try:
        municipio = (
            database.query(Municipio)
            .join(Estado)
            .filter(Municipio.estado_id == Estado.id)
            .filter(Estado.clave == estado_clave)
            .filter(Municipio.clave == municipio_clave)
            .filter(Estado.estatus == "A")
            .filter(Municipio.estatus == "A")
            .one()
        )
    except NoResultFound:
        raise MyNotExistsError("No existe ese municipio")
    if municipio.estatus != "A":
        raise MyIsDeletedError("No es activo ese municipio, está eliminado")
    return municipio
