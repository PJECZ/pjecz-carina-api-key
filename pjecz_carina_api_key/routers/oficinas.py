"""
Oficinas v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.oficinas import OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/v4/oficinas", tags=["categoria"])


def get_oficinas(database: Session) -> Any:
    """Consultar los oficinas activos"""
    consulta = database.query(Oficina)
    return consulta.filter_by(estatus="A").order_by(Oficina.id)


def get_oficina(database: Session, oficina_id: int) -> Oficina:
    """Consultar un oficina por su id"""
    oficina = database.query(Oficina).get(oficina_id)
    if oficina is None:
        raise MyNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise MyIsDeletedError("No es activo ese oficina, está eliminado")
    return oficina


@oficinas.get("/{oficina_id}", response_model=OneOficinaOut)
async def detalle_oficina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    oficina_id: int,
):
    """Detalle de una oficina a partir de su id"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina(database, oficina_id)
    except MyAnyError as error:
        return OneOficinaOut(success=False, message="Error al consultar la oficina", errors=[str(error)], data=None)
    return OneOficinaOut(
        success=True,
        message="Consulta hecha con éxito",
        errors=[],
        data=OficinaOut.model_validate(oficina),
    )


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def paginado_oficinas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_oficinas(database)
    except MyAnyError as error:
        return CustomPage(success=False, message="Error al consultar las oficinas", errors=[str(error)], data=None)
    return paginate(resultados)
