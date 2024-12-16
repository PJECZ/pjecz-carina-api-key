"""
Tareas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.core.tareas.models import Tarea  # Es necesario para que se reconozca el modelo
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.fastapi_not_implemented import NotImplement

tareas = APIRouter(prefix="/v4/tareas", tags=["usuarios"])


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
