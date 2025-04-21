"""
Domicilios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.domicilios import Domicilio
from ..models.permisos import Permiso
from ..schemas.domicilios import DomicilioOut, OneDomicilioOut

domicilios = APIRouter(prefix="/api/v5/domicilios")


@domicilios.get("/{domicilio_id}", response_model=OneDomicilioOut)
async def detalle_domicilio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    domicilio_id: int,
):
    """Detalle de un domicilio a partir de su id"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    domicilio = database.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        message = "No existe ese distrito"
        return OneDomicilioOut(success=False, message=message, errors=[message])
    if domicilio.estatus != "A":
        message = "No es activo ese domicilio, está eliminado"
        return OneDomicilioOut(success=False, message=message, errors=[message])
    return OneDomicilioOut(
        success=True,
        message=f"Detalle del domicilio {domicilio_id}",
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
    return paginate(database.query(Domicilio).filter_by(estatus="A").order_by(Domicilio.id))
