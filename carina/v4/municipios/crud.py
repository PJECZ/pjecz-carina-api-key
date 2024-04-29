"""
Municipios v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.municipios.models import Municipio


def get_municipios(database: Session) -> Any:
    """Consultar los municipios activos"""
    consulta = database.query(Municipio)
    return consulta.filter_by(estatus="A").order_by(Municipio.id)


def get_municipio(database: Session, municipio_id: int) -> Municipio:
    """Consultar un municipio por su id"""
    municipio = database.query(Municipio).get(municipio_id)
    if municipio is None:
        raise MyNotExistsError("No existe ese municipio")
    if municipio.estatus != "A":
        raise MyIsDeletedError("No es activo ese municipio, está eliminado")
    return municipio
