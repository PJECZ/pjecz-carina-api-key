"""
Oficinas
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.oficinas import OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/v5/oficinas", tags=["categoria"])


@oficinas.get("/{oficina_id}", response_model=OneOficinaOut)
async def detalle_oficina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    oficina_id: int,
):
    """Detalle de una oficina a partir de su id"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    oficina = database.query(Oficina).get(oficina_id)
    if oficina is None:
        message = "No existe ese distrito"
        return OneOficinaOut(success=False, message=message, errors=[message])
    if oficina.estatus != "A":
        message = "No es activo ese domicilio, está eliminado"
        return OneOficinaOut(success=False, message=message, errors=[message])
    return OneOficinaOut(
        success=True,
        message=f"Detalle del domicilio {oficina_id}",
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
    return paginate(database.query(Oficina).filter_by(estatus="A").order_by(Oficina.id))
