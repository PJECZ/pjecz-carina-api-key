"""
Estados v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from carina.core.permisos.models import Permiso
from carina.v4.estados.crud import get_estado_with_clave, get_estados
from carina.v4.estados.schemas import EstadoOut, OneEstadoOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

estados = APIRouter(prefix="/v4/estados", tags=["estados"])


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
        return OneEstadoOut(success=False, message="Error al consultar el estado", errors=[str(error)], data=None)
    return OneEstadoOut(success=True, message="Consulta hecha con éxito", errors=[], data=EstadoOut(**estado))


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
        return CustomList(success=False, message="Error al consultar los estados", errors=[str(error)], data=None)
    return paginate(resultados)
