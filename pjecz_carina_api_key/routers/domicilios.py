"""
Domicilios v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.domicilios import Domicilio
from ..models.permisos import Permiso
from ..schemas.domicilios import DomicilioOut, OneDomicilioOut

domicilios = APIRouter(prefix="/v4/domicilios", tags=["categoria"])


def get_domicilios(database: Session) -> Any:
    """Consultar los domicilio activos"""
    consulta = database.query(Domicilio)
    return consulta.filter_by(estatus="A").order_by(Domicilio.id)


def get_domicilio(database: Session, domicilio_id: int) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = database.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise MyNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise MyIsDeletedError("No es activo ese domicilio, está eliminado")
    return domicilio


@domicilios.get("/{domicilio_id}", response_model=OneDomicilioOut)
async def detalle_domicilio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    domicilio_id: int,
):
    """Detalle de una domicilio a partir de su id"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        domicilio = get_domicilio(database, domicilio_id)
    except MyAnyError as error:
        return OneDomicilioOut(success=False, message="Error al consultar el domicilio", errors=[str(error)], data=None)
    return OneDomicilioOut(
        success=True,
        message="Consulta hecha con éxito",
        errors=[],
        data=DomicilioOut.model_validate(domicilio),
    )


@domicilios.get("", response_model=CustomPage[DomicilioOut])
async def paginado_domicilios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de domicilios"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_domicilios(database)
    except MyAnyError as error:
        return CustomPage(success=False, message="Error al consultar los domicilios", errors=[str(error)], data=None)
    return paginate(resultados)
