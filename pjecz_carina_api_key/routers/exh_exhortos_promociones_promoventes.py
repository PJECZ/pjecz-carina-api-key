"""
Exh Exhortos Promociones Promoventes, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromovente  # Necesario para cargar este modelo
from ..models.permisos import Permiso

exh_exhortos_promociones_promoventes = APIRouter(prefix="/api/v5/exh_exhortos")


@exh_exhortos_promociones_promoventes.get("/promociones/promoventes", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar el JSON con success falso porque esta ruta no está implementada"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES PROMOVENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
