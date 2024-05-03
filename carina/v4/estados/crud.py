"""
Estados v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.estados.models import Estado


def get_estados(database: Session) -> Any:
    """Consultar los estados activos"""
    return database.query(Estado).filter_by(estatus="A").order_by(Estado.clave)


def get_estado(database: Session, estado_id: int) -> Estado:
    """Consultar un estado por su id"""
    estado = database.query(Estado).get(estado_id)
    if estado is None:
        raise MyNotExistsError("No existe ese estado")
    if estado.estatus != "A":
        raise MyIsDeletedError("No es activo ese estado, está eliminado")
    return estado
