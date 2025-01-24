"""
Exh Areas v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.exh_areas import ExhArea
from ..models.permisos import Permiso
from ..schemas.exh_areas import ExhAreaOut, OneExhAreaOut

exh_areas = APIRouter(prefix="/v4/exh_areas", tags=["exh areas"])


def get_exh_areas(database: Session) -> Any:
    """Consultar los áreas"""
    return database.query(ExhArea).filter_by(estatus="A").order_by(ExhArea.clave)


def get_exh_area(database: Session, exh_area_id: int) -> ExhArea:
    """Consultar un área por su id"""
    exh_area = database.query(ExhArea).get(exh_area_id)
    if exh_area is None:
        raise MyNotExistsError("No existe ese area")
    if exh_area.estatus != "A":
        raise MyIsDeletedError("No es activo ese area, está eliminado")
    return exh_area


def get_exh_area_with_clave(database: Session, exh_area_clave: str) -> ExhArea:
    """Consultar un area por su clave"""
    try:
        clave = safe_clave(exh_area_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    exh_area = database.query(ExhArea).filter_by(clave=clave).first()
    if exh_area is None:
        raise MyNotExistsError("No existe ese area")
    if exh_area.estatus != "A":
        raise MyIsDeletedError("No es activo ese area, está eliminado")
    return exh_area


@exh_areas.get("/{exh_area_clave}", response_model=OneExhAreaOut)
async def detalle_area(
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
        return OneExhAreaOut(success=False, message="Error al consultar el área", errors=[str(error)], data=None)
    return OneExhAreaOut(success=True, message="Consulta hecha con éxito", errors=[], data=ExhAreaOut.model_validate(exh_area))


@exh_areas.get("", response_model=CustomList[ExhAreaOut])
async def listado_areas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de areas"""
    if current_user.permissions.get("EXH AREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_exh_areas(database)
    except MyAnyError as error:
        return CustomList(success=False, message="Error al consultar las áreas", errors=[str(error)], data=None)
    return paginate(resultados)
