"""
Municipios v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from carina.core.permisos.models import Permiso
from carina.v4.municipios.crud import get_municipio_with_clave, get_municipios
from carina.v4.municipios.schemas import MunicipioOut, OneMunicipioOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

municipios = APIRouter(prefix="/v4/municipios", tags=["municipios"])


@municipios.get("/{estado_clave}/{municipio_clave}", response_model=OneMunicipioOut)
async def detalle_municipio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    estado_clave: str,
    municipio_clave: str,
):
    """Detalle de un municipio a partir las claves INEGI del estado y del municipio"""
    if current_user.permissions.get("MUNICIPIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        municipio = get_municipio_with_clave(database, estado_clave, municipio_clave)
    except MyAnyError as error:
        return OneMunicipioOut(success=False, message="Error al consultar el municipio", errors=[str(error)], data=None)
    return OneMunicipioOut(success=True, message="Consulta hecha con éxito", errors=[], data=OneMunicipioOut(**municipio))


@municipios.get("/{estado_clave}", response_model=CustomList[MunicipioOut])
async def listado_municipios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    estado_clave: str,
):
    """Listado de municipios"""
    if current_user.permissions.get("MUNICIPIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_municipios(database, estado_clave)
    except MyAnyError as error:
        return CustomList(success=False, message="Error al consultar los municipios", errors=[str(error)], data=None)
    return paginate(resultados)
