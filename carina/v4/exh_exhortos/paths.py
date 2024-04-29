"""
Exh Exhortos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_exhortos, get_exh_exhorto
from .schemas import ExhExhortoOut, OneExhExhortoOut

exh_exhortos = APIRouter(prefix="/v4/exh_exhortos", tags=["exhortos"])


@exh_exhortos.get("", response_model=CustomPage[ExhExhortoOut])
async def paginado_exh_exhortos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de exhortos"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_exh_exhortos(database)
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@exh_exhortos.get("/{exh_exhorto_id}", response_model=OneExhExhortoOut)
async def detalle_exh_exhorto(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_id: int,
):
    """Detalle de una exhorto a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    except MyAnyError as error:
        return OneExhExhortoOut(success=False, errors=[str(error)])
    return OneExhExhortoOut.model_validate(exh_exhorto)
