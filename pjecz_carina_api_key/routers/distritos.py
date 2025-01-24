"""
Distritos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.distritos import Distrito
from ..models.permisos import Permiso
from ..schemas.distritos import DistritoOut, OneDistritoOut

distritos = APIRouter(prefix="/v4/distritos", tags=["distritos"])


def get_distritos(
    database: Session,
    es_distrito: bool = None,
    es_jurisdiccional: bool = None,
) -> Any:
    """Consultar los distritos activos"""
    consulta = database.query(Distrito)
    if es_distrito is not None:
        consulta = consulta.filter_by(es_distrito=es_distrito)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    return consulta.filter_by(estatus="A").order_by(Distrito.clave)


def get_distrito(database: Session, distrito_id: int) -> Distrito:
    """Consultar un distrito por su id"""
    distrito = database.query(Distrito).get(distrito_id)
    if distrito is None:
        raise MyNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise MyIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito


def get_distrito_with_clave(database: Session, distrito_clave: str) -> Distrito:
    """Consultar un distrito por su clave"""
    try:
        clave = safe_clave(distrito_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    distrito = database.query(Distrito).filter_by(clave=clave).first()
    if distrito is None:
        raise MyNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise MyIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito


@distritos.get("/{distrito_clave}", response_model=OneDistritoOut)
async def detalle_distrito(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_clave: str,
):
    """Detalle de una distrito a partir de su clave"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        distrito = get_distrito_with_clave(database, distrito_clave)
    except MyAnyError as error:
        return OneDistritoOut(success=False, message="Error al consultar el distrito", errors=[str(error)], data=None)
    return OneDistritoOut(
        success=True,
        message="Consulta hecha con éxito",
        errors=[],
        data=DistritoOut.model_validate(distrito),
    )


@distritos.get("", response_model=CustomList[DistritoOut])
async def paginado_distritos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    es_distrito: bool = None,
    es_jurisdiccional: bool = None,
):
    """Paginado de distritos"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_distritos(
            database=database,
            es_distrito=es_distrito,
            es_jurisdiccional=es_jurisdiccional,
        )
    except MyAnyError as error:
        return CustomList(success=False, message="Error al consultar los distritos", errors=[str(error)], data=None)
    return paginate(resultados)
