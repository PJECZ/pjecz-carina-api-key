"""
Municipios v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.estados import Estado
from ..models.municipios import Municipio
from ..models.permisos import Permiso
from ..schemas.municipios import MunicipioOut, OneMunicipioOut
from .estados import get_estado_with_clave

municipios = APIRouter(prefix="/v4/municipios", tags=["municipios"])


def get_municipios(database: Session, estado_clave: str = None) -> Any:
    """Consultar los municipios"""
    try:
        estado_clave = safe_clave(estado_clave).zfill(2)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    consulta = database.query(Municipio)
    if estado_clave is not None:
        estado = get_estado_with_clave(database, estado_clave)
        consulta = consulta.filter_by(estado_id=estado.id)
    return consulta.filter_by(estatus="A").order_by(Municipio.clave)


def get_municipio(database: Session, municipio_id: int) -> Municipio:
    """Consultar un municipio por su id"""
    municipio = database.query(Municipio).get(municipio_id)
    if municipio is None:
        raise MyNotExistsError("No existe ese municipio")
    if municipio.estatus != "A":
        raise MyIsDeletedError("No es activo ese municipio, está eliminado")
    return municipio


def get_municipio_with_clave(database: Session, estado_clave: str, municipio_clave: str) -> Municipio:
    """Consultar un municipio por su clave y la clave de su estado"""
    try:
        estado_clave = safe_clave(estado_clave).zfill(2)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    try:
        municipio_clave = safe_clave(municipio_clave).zfill(3)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    municipio = (
        database.query(Municipio)
        .join(Estado)
        .filter(Municipio.estado_id == Estado.id)
        .filter(Estado.clave == estado_clave)
        .filter(Municipio.clave == municipio_clave)
        .filter(Estado.estatus == "A")
        .filter(Municipio.estatus == "A")
        .first()
    )
    if municipio is None:
        raise MyNotExistsError("No existe ese municipio")
    if municipio.estatus != "A":
        raise MyIsDeletedError("No es activo ese municipio, está eliminado")
    return municipio


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
    return OneMunicipioOut(
        success=True,
        message="Consulta hecha con éxito",
        errors=[],
        data=MunicipioOut.model_validate(municipio),
    )


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
