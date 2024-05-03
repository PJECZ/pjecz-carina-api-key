"""
Municipios v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_municipios, get_municipio
from .schemas import MunicipioOut, OneMunicipioOut

municipios = APIRouter(prefix="/v4/municipios", tags=["categoria"])


@municipios.get("", response_model=CustomPage[MunicipioOut])
async def paginado_municipios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de municipios"""
    if current_user.permissions.get("MUNICIPIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_municipios(database)
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@municipios.get("/{municipio_id}", response_model=OneMunicipioOut)
async def detalle_municipio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    municipio_id: int,
):
    """Detalle de una municipio a partir de su id"""
    if current_user.permissions.get("MUNICIPIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        municipio = get_municipio(database, municipio_id)
    except MyAnyError as error:
        return OneMunicipioOut(success=False, errors=[str(error)])
    return OneMunicipioOut.model_validate(municipio)
