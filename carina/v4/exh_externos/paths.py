"""
Exh Externos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.fastapi_not_implemented import NotImplement

exh_externos = APIRouter(prefix="/v4/exh_externos", tags=["exh externos"])


@exh_externos.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Detalle de un video a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS VIDEOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
