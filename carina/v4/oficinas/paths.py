"""
Oficinas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_oficina, get_oficinas
from .schemas import OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/v4/oficinas", tags=["categoria"])


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def paginado_oficinas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_oficinas(database)
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@oficinas.get("/{oficina_id}", response_model=OneOficinaOut)
async def detalle_oficina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    oficina_id: int,
):
    """Detalle de una oficina a partir de su id"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina(database, oficina_id)
    except MyAnyError as error:
        return OneOficinaOut(success=False, errors=[str(error)])
    return OneOficinaOut.model_validate(oficina)
