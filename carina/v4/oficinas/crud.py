"""
Oficinas v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.oficinas.models import Oficina


def get_oficinas(database: Session) -> Any:
    """Consultar los oficinas activos"""
    consulta = database.query(Oficina)
    return consulta.filter_by(estatus="A").order_by(Oficina.id)


def get_oficina(database: Session, oficina_id: int) -> Oficina:
    """Consultar un oficina por su id"""
    oficina = database.query(Oficina).get(oficina_id)
    if oficina is None:
        raise MyNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise MyIsDeletedError("No es activo ese oficina, está eliminado")
    return oficina
