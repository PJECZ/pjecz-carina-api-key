"""
Domicilios v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from carina.core.permisos.models import Permiso
from carina.v4.domicilios.crud import get_domicilio, get_domicilios
from carina.v4.domicilios.schemas import DomicilioOut, OneDomicilioOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

domicilios = APIRouter(prefix="/v4/domicilios", tags=["categoria"])


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
