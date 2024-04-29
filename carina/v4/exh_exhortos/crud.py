"""
Exh Exhortos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.exh_exhortos.models import ExhExhorto


def get_exh_exhortos(database: Session) -> Any:
    """Consultar los exhortos activos"""
    consulta = database.query(ExhExhorto)
    return consulta.filter_by(estatus="A").order_by(ExhExhorto.id)


def get_exh_exhorto(database: Session, exh_exhorto_id: int) -> ExhExhorto:
    """Consultar un exhorto por su id"""
    exh_exhorto = database.query(ExhExhorto).get(exh_exhorto_id)
    if exh_exhorto is None:
        raise MyNotExistsError("No existe ese exhorto")
    if exh_exhorto.estatus != "A":
        raise MyIsDeletedError("No es activo ese exhorto, está eliminado")
    return exh_exhorto
