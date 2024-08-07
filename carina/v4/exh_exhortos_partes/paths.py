"""
Exh Exhortos Partes v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_exhorto_parte
from .schemas import OneExhExhortoParteOut

exh_exhortos_partes = APIRouter(prefix="/v4/exh_exhortos_partes", tags=["exhortos"])


@exh_exhortos_partes.get("/{exh_exhorto_parte_id}", response_model=OneExhExhortoParteOut)
async def detalle_exh_exhorto_parte(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_parte_id: int,
):
    """Detalle de una parte a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS PARTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_parte = get_exh_exhorto_parte(database, exh_exhorto_parte_id)
    except MyAnyError as error:
        return OneExhExhortoParteOut(success=False, errors=[str(error)])
    return OneExhExhortoParteOut(success=True, data=exh_exhorto_parte)
