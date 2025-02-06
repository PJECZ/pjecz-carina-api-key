"""
Municipios
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.estados import Estado
from ..models.municipios import Municipio
from ..models.permisos import Permiso
from ..schemas.municipios import MunicipioOut, OneMunicipioOut

municipios = APIRouter(prefix="/v5/municipios", tags=["municipios"])


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
        estado_clave = safe_clave(estado_clave).zfill(2)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del estado")
    try:
        municipio_clave = safe_clave(municipio_clave).zfill(3)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del municipio")
    try:
        municipio = (
            database.query(Municipio)
            .join(Estado)
            .filter(Estado.clave == estado_clave)
            .filter(Municipio.clave == municipio_clave)
            .one()
        )
    except (MultipleResultsFound, NoResultFound) as error:
        return OneMunicipioOut(success=False, message="No existe ese municipio", errors=[str(error)])
    return OneMunicipioOut(success=True, message="Detalle del municipio", data=MunicipioOut.model_validate(municipio))


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
        estado_clave = safe_clave(estado_clave).zfill(2)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del estado")
    return paginate(database.query(Municipio).join(Estado).filter(Estado.clave == estado_clave).order_by(Municipio.clave))
