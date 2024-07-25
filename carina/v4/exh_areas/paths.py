"""
Exh Areas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_area_with_clave, get_exh_areas
from .schemas import ExhAreaOut, OneExhAreaOut

exh_areas = APIRouter(prefix="/v4/exh_areas", tags=["exhortos"])


@exh_areas.get("", response_model=CustomList[ExhAreaOut])
async def listado_exh_areas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de areas"""
    if current_user.permissions.get("EXH AREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_exh_areas(database)
    except MyAnyError as error:
        return CustomList(success=False, errors=[str(error)])
    return paginate(resultados)


@exh_areas.get("/{exh_area_clave}", response_model=OneExhAreaOut)
async def detalle_exh_area(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_area_clave: str,
):
    """Detalle de un area a partir de su clave"""
    if current_user.permissions.get("EXH AREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_area = get_exh_area_with_clave(database, exh_area_clave)
    except MyAnyError as error:
        return OneExhAreaOut(success=False, errors=[str(error)])
    return OneExhAreaOut(success=True, data=exh_area)
