"""
Exh Tipos Diligencias, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.exh_tipos_diligencias import ExhTipoDiligencia
from ..models.permisos import Permiso
from ..schemas.exh_tipos_diligencias import ExhTipoDiligenciaOut, OneExhTipoDiligenciaOut
from ..settings import Settings, get_settings

exh_tipos_diligencias = APIRouter(prefix="/api/v5/exh_tipos_diligencias")


def get_exh_tipo_diligencia_with_clave_otr(database: Annotated[Session, Depends(get_db)]) -> ExhTipoDiligencia:
    """Consultar el tipo de diligencia con clave OTR"""
    try:
        return database.query(ExhTipoDiligencia).filter_by(clave="OTR").one()
    except (MultipleResultsFound, NoResultFound) as error:
        raise MyNotExistsError("No existe el tipo de diligencia con clave OTR") from error


@exh_tipos_diligencias.get("/{clave}", response_model=ExhTipoDiligenciaOut)
async def detalle_exh_tipo_diligencia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de un tipo de diligencia a partir de su clave"""
    if current_user.permissions.get("EXH TIPOS DILIGENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        exh_tipo_diligencia = database.query(ExhTipoDiligencia).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneExhTipoDiligenciaOut(success=False, message="No existe esa área", errors=[str(error)])
    if exh_tipo_diligencia.estatus != "A":
        message = "No está habilitado ese tipo de diligencia"
        return OneExhTipoDiligenciaOut(success=False, message=message, errors=[message])
    return OneExhTipoDiligenciaOut(
        success=True, message=f"Detalle de {clave}", data=ExhTipoDiligenciaOut.model_validate(exh_tipo_diligencia)
    )


@exh_tipos_diligencias.get("", response_model=CustomList[ExhTipoDiligenciaOut])
async def listado_exh_tipos_diligencias(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de tipos de diligencias"""
    if current_user.permissions.get("EXH TIPOS DILIGENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(ExhTipoDiligencia).filter_by(estatus="A").order_by(ExhTipoDiligencia.clave))
