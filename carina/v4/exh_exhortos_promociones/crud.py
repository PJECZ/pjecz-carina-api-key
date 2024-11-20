"""
Exh Exhortos Promociones v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_exhortos_promociones.models import ExhExhortoPromocion
from carina.v4.exh_exhortos.crud import get_exh_exhorto
from lib.exceptions import MyIsDeletedError, MyNotExistsError


def get_exh_exhortos_promociones(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar las promociones de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoPromocion)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoPromocion.id)
    )


def get_exh_exhorto_promocion(database: Session, exh_exhorto_promocion_id: int) -> ExhExhortoPromocion:
    """Consultar una promoción de un exhorto por su id"""
    exh_exhorto_promocion = database.query(ExhExhortoPromocion).get(exh_exhorto_promocion_id)
    if exh_exhorto_promocion is None:
        raise MyNotExistsError("No existe esa promoción de exhorto")
    if exh_exhorto_promocion.estatus != "A":
        raise MyIsDeletedError("No es activa esa promoción de exhorto, está eliminada")
    return exh_exhorto_promocion
