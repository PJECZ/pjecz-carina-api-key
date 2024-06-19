"""
Domicilios v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.domicilios.models import Domicilio


def get_domicilios(database: Session) -> Any:
    """Consultar los domicilio activos"""
    consulta = database.query(Domicilio)
    return consulta.filter_by(estatus="A").order_by(Domicilio.id)


def get_domicilio(database: Session, domicilio_id: int) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = database.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise MyNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise MyIsDeletedError("No es activo ese domicilio, está eliminado")
    return domicilio
