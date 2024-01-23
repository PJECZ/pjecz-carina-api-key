"""
Tareas v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_tareas, get_tarea
from .schemas import TareaOut, OneTareaOut

tareas = APIRouter(prefix="/v4/tareas", tags=["usuarios"])


@tareas.get("", response_model=CustomPage[TareaOut])
async def paginado_tareas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Paginado de tareas"""
    if current_user.permissions.get("TAREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_tareas(
            database=database,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@tareas.get("/{tarea_id}", response_model=OneTareaOut)
async def detalle_tarea(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    tarea_id: int,
):
    """Detalle de una tarea a partir de su id"""
    if current_user.permissions.get("TAREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        tarea = get_tarea(database, tarea_id)
    except MyAnyError as error:
        return OneTareaOut(success=False, errors=[str(error)])
    return OneTareaOut.model_validate(tarea)
