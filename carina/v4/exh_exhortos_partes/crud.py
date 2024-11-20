"""
Exh Exhorto Partes v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_exhortos_partes.models import ExhExhortoParte
from carina.v4.exh_exhortos.crud import get_exh_exhorto
from lib.exceptions import MyIsDeletedError, MyNotExistsError


def get_exh_exhortos_partes(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar los partes de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoParte)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoParte.id)
    )


def get_exh_exhorto_parte(database: Session, exh_exhorto_parte_id: int) -> ExhExhortoParte:
    """Consultar una parte por su id"""
    exh_exhorto_parte = database.query(ExhExhortoParte).get(exh_exhorto_parte_id)
    if exh_exhorto_parte is None:
        raise MyNotExistsError("No existe ese parte")
    if exh_exhorto_parte.estatus != "A":
        raise MyIsDeletedError("No es activo ese parte, está eliminado")
    return exh_exhorto_parte
