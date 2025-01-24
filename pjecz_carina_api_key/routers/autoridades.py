"""
Autoridades v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.permisos import Permiso
from ..schemas.autoridades import AutoridadOut, OneAutoridadOut
from .distritos import get_distrito, get_distrito_with_clave

autoridades = APIRouter(prefix="/v4/autoridades", tags=["autoridades"])


def get_autoridades(
    database: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    es_extinto: bool = None,
) -> Any:
    """Consultar las autoridades"""
    consulta = database.query(Autoridad)
    if distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if es_extinto is not None:
        consulta = consulta.filter_by(es_extinto=es_extinto)
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave)


def get_autoridad(database: Session, autoridad_id: int) -> Autoridad:
    """Consultar una autoridad por su id"""
    autoridad = database.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad


def get_autoridad_with_clave(database: Session, autoridad_clave: str) -> Autoridad:
    """Consultar una autoridad por su clave"""
    try:
        clave = safe_clave(autoridad_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    autoridad = database.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad


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
    return OneAutoridadOut(
        success=True,
        message="Consulta hecha con éxito",
        errors=[],
        data=AutoridadOut.model_validate(autoridad),
    )


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
