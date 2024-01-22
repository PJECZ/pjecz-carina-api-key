"""
Modulos v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_modulos, get_modulo
from .schemas import ModuloOut, OneModuloOut

modulos = APIRouter(prefix="/v4/modulos", tags=["usuarios"])


@modulos.get("", response_model=CustomPage[ModuloOut])
async def paginado_modulos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de modulos"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_modulos(database)
    except MyAnyError as error:
        return CustomPage(success=False, errors=str(error))
    return paginate(resultados)


@modulos.get("/{modulo_id}", response_model=OneModuloOut)
async def detalle_modulo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    modulo_id: int,
):
    """Detalle de un modulo a partir de su id"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        modulo = get_modulo(database, modulo_id)
    except MyAnyError as error:
        return OneModuloOut(success=False, errors=str(error))
    return OneModuloOut.model_validate(modulo)
