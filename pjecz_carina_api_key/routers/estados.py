"""
Estados v4, rutas (paths)
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
from ..models.permisos import Permiso
from ..schemas.estados import EstadoOut, OneEstadoOut

estados = APIRouter(prefix="/v4/estados", tags=["estados"])


def get_estados(database: Session) -> Any:
    """Consultar los estados"""
    return database.query(Estado).filter_by(estatus="A").order_by(Estado.clave)


def get_estado(database: Session, estado_id: int) -> Estado:
    """Consultar un estado por su id"""
    estado = database.query(Estado).get(estado_id)
    if estado is None:
        raise MyNotExistsError("No existe ese estado")
    if estado.estatus != "A":
        raise MyIsDeletedError("No es activo ese estado, está eliminado")
    return estado


def get_estado_with_clave(database: Session, estado_clave: str) -> Estado:
    """Consultar un estado por su clave"""
    try:
        clave = safe_clave(estado_clave).zfill(2)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    estado = database.query(Estado).filter_by(clave=clave).first()
    if estado is None:
        raise MyNotExistsError("No existe ese estado")
    if estado.estatus != "A":
        raise MyIsDeletedError("No es activo ese estado, está eliminado")
    return estado


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
    return OneEstadoOut(success=True, message="Consulta hecha con éxito", errors=[], data=EstadoOut.model_validate(estado))


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
