"""
Materias v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.materias import Materia
from ..models.permisos import Permiso
from ..schemas.materias import MateriaOut, OneMateriaOut

materias = APIRouter(prefix="/v4/materias", tags=["materias"])


def get_materias(database: Session) -> Any:
    """Consultar las materias"""
    return database.query(Materia).filter_by(estatus="A").filter_by(en_exh_exhortos=True).order_by(Materia.clave)


def get_materia(database: Session, materia_id: int) -> Materia:
    """Consultar una materia por su id"""
    materia = database.query(Materia).get(materia_id)
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activa esa materia, está eliminada")
    if materia.en_exh_exhortos is False:
        raise MyNotExistsError("No se usa esa materia en exhortos electrónicos")
    return materia


def get_materia_with_clave(database: Session, materia_clave: str) -> Materia:
    """Consultar una materia por su clave"""
    try:
        clave = safe_clave(materia_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    materia = database.query(Materia).filter_by(clave=clave).first()
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia, está eliminado")
    if materia.en_exh_exhortos is False:
        raise MyNotExistsError("No se usa esa materia en exhortos electrónicos")
    return materia


@materias.get("/{materia_clave}", response_model=OneMateriaOut)
async def detalle_materia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    materia_clave: str,
):
    """Detalle de una materia a partir de su clave"""
    if current_user.permissions.get("MATERIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        materia = get_materia_with_clave(database, materia_clave)
    except MyAnyError as error:
        return OneMateriaOut(success=False, message="Error al consultar la materia", errors=[str(error)], data=None)
    return OneMateriaOut(success=True, message="Consulta hecha con éxito", errors=[], data=MateriaOut.model_validate(materia))


@materias.get("", response_model=CustomList[MateriaOut])
async def listado_materias(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Listado de materias"""
    if current_user.permissions.get("MATERIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_materias(database)
    except MyAnyError as error:
        return CustomList(success=False, message="Error al consultar las materias", errors=[str(error)], data=None)
    return paginate(resultados)
