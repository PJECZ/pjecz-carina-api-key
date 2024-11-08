"""
Estados v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_estado_with_clave, get_estados
from .schemas import EstadoOut, OneEstadoOut

estados = APIRouter(prefix="/v4/estados", tags=["estados"])


@estados.get("", response_model=CustomList[EstadoOut])
async def listado_estados(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Listado de estados"""
    if current_user.permissions.get("ESTADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_estados(database)
    except MyAnyError as error:
        return CustomList(success=False, errors=[str(error)])
    return paginate(resultados)


@estados.get("/{estado_clave}", response_model=OneEstadoOut)
async def detalle_estado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    estado_clave: str,
):
    """Detalle de un estado a partir de su clave INEGI"""
    if current_user.permissions.get("ESTADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        estado = get_estado_with_clave(database, estado_clave)
    except MyAnyError as error:
        return OneEstadoOut(success=False, errors=[str(error)])
    return OneEstadoOut(success=True, data=estado)
