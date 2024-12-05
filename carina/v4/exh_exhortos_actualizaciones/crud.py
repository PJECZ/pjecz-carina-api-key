"""
Exh Exhortos Actualizaciones v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_exhortos_actualizaciones.models import ExhExhortoActualizacion
from carina.v4.exh_exhortos.crud import get_exh_exhorto
from lib.exceptions import MyIsDeletedError, MyNotExistsError


def get_exh_exhortos_actualizaciones(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar las actualizaciones de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoActualizacion)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoActualizacion.id)
    )


def get_exh_exhorto_actualizacion(database: Session, exh_exhorto_actualizacion_id: int) -> ExhExhortoActualizacion:
    """Consultar una actualización de un exhorto por su id"""
    exh_exhorto_actualizacion = database.query(ExhExhortoActualizacion).get(exh_exhorto_actualizacion_id)
    if exh_exhorto_actualizacion is None:
        raise MyNotExistsError("No existe esa actualización de exhorto")
    if exh_exhorto_actualizacion.estatus != "A":
        raise MyIsDeletedError("No es activa esa actualización de exhorto, está eliminada")
    return exh_exhorto_actualizacion


def create_exh_exhorto_actualizacion(database: Session, exh_exhorto_actualizacion: ExhExhortoActualizacion):
    """Crear una actualización de un exhorto"""
