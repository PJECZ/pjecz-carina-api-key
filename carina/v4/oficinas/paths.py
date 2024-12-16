"""
Oficinas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from carina.core.permisos.models import Permiso
from carina.v4.oficinas.crud import get_oficina, get_oficinas
from carina.v4.oficinas.schemas import OficinaOut, OneOficinaOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

oficinas = APIRouter(prefix="/v4/oficinas", tags=["categoria"])


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
