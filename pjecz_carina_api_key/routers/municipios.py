"""
Municipios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.estados import Estado
from ..models.municipios import Municipio
from ..models.permisos import Permiso
from ..schemas.municipios import MunicipioOut, OneMunicipioOut
from ..settings import Settings, get_settings

municipios = APIRouter(prefix="/api/v5/municipios")


def get_municipio_destino(
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    municipio_num: int,
) -> Municipio:
    """Obtener el municipio de destino a partir de la clave INEGI"""
    municipio_destino_clave = str(municipio_num).zfill(3)
    try:
        municipio_destino = (
            database.query(Municipio).filter_by(estado_id=settings.estado_clave).filter_by(clave=municipio_destino_clave).one()
        )
    except (MultipleResultsFound, NoResultFound) as error:
        raise MyNotExistsError(
            f"No existe el municipio {municipio_destino_clave} en el estado {settings.estado_clave}"
        ) from error
    return municipio_destino


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


def get_municipio_origen(database: Annotated[Session, Depends(get_db)], estado_num: int, municipio_num: int) -> Municipio:
    """Obtener el municipio de destino a partir de la clave INEGI"""
    estado_origen_clave = str(estado_num).zfill(2)
    try:
        estado_origen = database.query(Estado).filter_by(clave=estado_origen_clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        raise MyNotExistsError(f"No existe el estado {estado_origen_clave}") from error
    municipio_origen_clave = str(municipio_num).zfill(3)
    try:
        municipio_origen = (
            database.query(Municipio).filter_by(estado_id=estado_origen.id).filter_by(clave=municipio_origen_clave).one()
        )
    except (MultipleResultsFound, NoResultFound) as error:
        raise MyNotExistsError(f"No existe el municipio {municipio_origen_clave} en {estado_origen_clave}") from error
    return municipio_origen


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
