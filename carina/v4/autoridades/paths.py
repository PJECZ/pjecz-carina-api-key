"""
Autoridades v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from carina.core.permisos.models import Permiso
from carina.v4.autoridades.crud import get_autoridad_with_clave, get_autoridades
from carina.v4.autoridades.schemas import AutoridadOut, OneAutoridadOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

autoridades = APIRouter(prefix="/v4/autoridades", tags=["autoridades"])


@autoridades.get("/{autoridad_clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        autoridad = get_autoridad_with_clave(database, autoridad_clave)
    except MyAnyError as error:
        return OneAutoridadOut(success=False, message="Error al consultar la autoridad", errors=[str(error)], data=None)
    return OneAutoridadOut(success=True, message="Consulta hecha con éxito", errors=[], data=AutoridadOut(**autoridad))


@autoridades.get("", response_model=CustomList[AutoridadOut])
async def paginado_autoridades(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_id: int = None,
    distrito_clave: str = None,
    es_extinto: bool = None,
):
    """Paginado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_autoridades(
            database=database,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            es_extinto=es_extinto,
        )
    except MyAnyError as error:
        return CustomList(success=False, message="Error al consultar las autoridades", errors=[str(error)], data=None)
    return paginate(resultados)
