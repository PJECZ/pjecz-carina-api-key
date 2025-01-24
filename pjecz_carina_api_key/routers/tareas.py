"""
Tareas v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.permisos import Permiso
from ..models.tareas import Tarea
from .usuarios import get_usuario, get_usuario_with_email

tareas = APIRouter(prefix="/v4/tareas", tags=["usuarios"])


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


@tareas.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("TAREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
