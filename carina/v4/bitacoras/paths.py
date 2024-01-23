"""
Bitacoras v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_bitacoras, get_bitacora
from .schemas import BitacoraOut, OneBitacoraOut

bitacoras = APIRouter(prefix="/v4/bitacoras", tags=["usuarios"])


@bitacoras.get("", response_model=CustomPage[BitacoraOut])
async def paginado_bitacoras(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    modulo_id: int = None,
    modulo_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Paginado de bitacoras"""
    if current_user.permissions.get("BITACORAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_bitacoras(
            database=database,
            modulo_id=modulo_id,
            modulo_nombre=modulo_nombre,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@bitacoras.get("/{bitacora_id}", response_model=OneBitacoraOut)
async def detalle_bitacora(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    bitacora_id: int,
):
    """Detalle de una bitacora a partir de su id"""
    if current_user.permissions.get("BITACORAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        bitacora = get_bitacora(database, bitacora_id)
    except MyAnyError as error:
        return OneBitacoraOut(success=False, errors=[str(error)])
    return OneBitacoraOut.model_validate(bitacora)
