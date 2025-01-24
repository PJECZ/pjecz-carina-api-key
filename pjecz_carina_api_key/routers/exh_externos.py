"""
Exh Externos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..dependencies.safe_string import safe_clave
from ..models.exh_externos import ExhExterno
from ..models.permisos import Permiso

exh_externos = APIRouter(prefix="/v4/exh_externos", tags=["exh externos"])


def get_exh_externos(database: Session) -> Any:
    """Consultar los externos activos"""
    return database.query(ExhExterno).filter_by(estatus="A").order_by(ExhExterno.clave)


def get_exh_externo(database: Session, exh_externo_id: int) -> ExhExterno:
    """Consultar un externo por su id"""
    exh_externo = database.query(ExhExterno).get(exh_externo_id)
    if exh_externo is None:
        raise MyNotExistsError("No existe ese externo")
    if exh_externo.estatus != "A":
        raise MyIsDeletedError("No es activo ese externo, está eliminado")
    return exh_externo


def get_exh_externo_with_clave(database: Session, exh_externo_clave: str) -> ExhExterno:
    """Consultar un externo por su clave"""
    try:
        exh_externo_clave = safe_clave(exh_externo_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    exh_externo = database.query(ExhExterno).filter_by(clave=exh_externo_clave).first()
    if exh_externo is None:
        raise MyNotExistsError("No existe ese externo")
    if exh_externo.estatus != "A":
        raise MyIsDeletedError("No es activo ese externo, está eliminado")
    return exh_externo


@exh_externos.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Detalle de un video a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS VIDEOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
