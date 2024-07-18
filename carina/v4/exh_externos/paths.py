"""
Exh Externos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_externo_with_clave
from .schemas import OneExhExternoOut

exh_externos = APIRouter(prefix="/v4/exh_externos", tags=["externos"])


@exh_externos.get("/{exh_externo_clave}", response_model=OneExhExternoOut)
async def detalle_exh_externo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_externo_clave: str,
):
    """Detalle de un video a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS VIDEOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_externo = get_exh_externo_with_clave(database, exh_externo_clave)
    except MyAnyError as error:
        return OneExhExternoOut(success=False, errors=[str(error)])
    return OneExhExternoOut(success=True, data=exh_externo)
