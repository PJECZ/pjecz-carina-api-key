"""
Exh Areas
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.exh_areas import ExhArea
from ..models.permisos import Permiso
from ..schemas.exh_areas import ExhAreaOut, OneExhAreaOut

exh_areas = APIRouter(prefix="/api/v5/exh_areas")


@exh_areas.get("/{clave}", response_model=OneExhAreaOut)
async def detalle_area(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de un area a partir de su clave"""
    if current_user.permissions.get("EXH AREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        exh_area = database.query(ExhArea).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneExhAreaOut(success=False, message="No existe esa área", errors=[str(error)])
    if exh_area.estatus != "A":
        message = "No está habilitada esa área"
        return OneExhAreaOut(success=False, message=message, errors=[message])
    return OneExhAreaOut(success=True, message=f"Detalle de {clave}", data=ExhAreaOut.model_validate(exh_area))


@exh_areas.get("", response_model=CustomList[ExhAreaOut])
async def listado_areas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de areas"""
    if current_user.permissions.get("EXH AREAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(ExhArea).filter_by(estatus="A").order_by(ExhArea.clave))
