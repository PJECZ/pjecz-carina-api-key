"""
Estados
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.estados import Estado
from ..models.permisos import Permiso
from ..schemas.estados import EstadoOut, OneEstadoOut

estados = APIRouter(prefix="/v5/estados", tags=["estados"])


@estados.get("/{clave}", response_model=OneEstadoOut)
async def detalle_estado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de un estado a partir de su clave INEGI"""
    if current_user.permissions.get("ESTADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave).zfill(2)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        estado = database.query(Estado).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneEstadoOut(success=False, message="No existe ese estado", errors=[str(error)])
    if estado.estatus != "A":
        message = "No está habilitado ese estado"
        return OneEstadoOut(success=False, message=message, errors=[message])
    return OneEstadoOut(success=True, message=f"Detalle de {clave}", data=EstadoOut.model_validate(estado))


@estados.get("", response_model=CustomList[EstadoOut])
async def listado_estados(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Listado de estados"""
    if current_user.permissions.get("ESTADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Estado).filter_by(estatus="A").order_by(Estado.clave))
