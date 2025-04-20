"""
Entradas-Salidas, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.entradas_salidas import EntradaSalida  # Necesario para cargar este modelo
from ..models.permisos import Permiso

entradas_salidas = APIRouter(prefix="/api/v5/entradas_salidas")


@entradas_salidas.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar el JSON con success falso porque esta ruta no está implementada"""
    if current_user.permissions.get("ENTRADAS SALIDAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
