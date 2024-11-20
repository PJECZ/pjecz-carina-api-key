"""
Exh Exhortos Promociones Promoventes v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_exhortos_promociones_promoventes.models import ExhExhortoPromocionPromovente
from carina.v4.exh_exhortos_promociones.crud import get_exh_exhorto_promocion
from lib.exceptions import MyIsDeletedError, MyNotExistsError


def get_exh_exhortos_promociones_promoventes(database: Session, exh_exhorto_promocion_id: int) -> Any:
    """Consultar los promoventes de una promoción de un exhorto"""
    exh_exhorto_promocion = get_exh_exhorto_promocion(database, exh_exhorto_promocion_id)
    return (
        database.query(ExhExhortoPromocionPromovente)
        .filter_by(exh_exhorto_promocion_id=exh_exhorto_promocion.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoPromocionPromovente.id)
    )


def get_exh_exhorto_promocion_promovente(
    database: Session, exh_exhorto_promocion_promovente_id: int
) -> ExhExhortoPromocionPromovente:
    """Consultar un promovente de una promoción de un exhorto por su id"""
    exh_exhorto_promocion_promovente = database.query(ExhExhortoPromocionPromovente).get(exh_exhorto_promocion_promovente_id)
    if exh_exhorto_promocion_promovente is None:
        raise MyNotExistsError("No existe ese promovente de promoción de exhorto")
    if exh_exhorto_promocion_promovente.estatus != "A":
        raise MyIsDeletedError("No es activo ese promovente de promoción de exhorto, está eliminado")
    return exh_exhorto_promocion_promovente
