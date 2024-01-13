"""
Tareas v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.tareas.models import Tarea
from ..usuarios.crud import get_usuario, get_usuario_with_email


def get_tareas(
    database: Session,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los tareas activos"""
    consulta = database.query(Tarea)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    elif usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return consulta.filter_by(estatus="A").order_by(Tarea.id)


def get_tarea(database: Session, tarea_id: int) -> Tarea:
    """Consultar un tarea por su id"""
    tarea = database.query(Tarea).get(tarea_id)
    if tarea is None:
        raise MyNotExistsError("No existe ese tarea")
    if tarea.estatus != "A":
        raise MyIsDeletedError("No es activo ese tarea, está eliminado")
    return tarea
