"""
Exh Exhortos Partes v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.exh_exhortos_partes import ExhExhortoParte
from ..models.permisos import Permiso
from .exh_exhortos import get_exh_exhorto

exh_exhortos_partes = APIRouter(prefix="/v4/exh_exhortos_partes", tags=["exh exhortos"])


def get_exh_exhortos_partes(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar los partes de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoParte)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoParte.id)
    )


def get_exh_exhorto_parte(database: Session, exh_exhorto_parte_id: int) -> ExhExhortoParte:
    """Consultar una parte por su id"""
    exh_exhorto_parte = database.query(ExhExhortoParte).get(exh_exhorto_parte_id)
    if exh_exhorto_parte is None:
        raise MyNotExistsError("No existe ese parte")
    if exh_exhorto_parte.estatus != "A":
        raise MyIsDeletedError("No es activo ese parte, está eliminado")
    return exh_exhorto_parte


@exh_exhortos_partes.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("EXH EXHORTOS PARTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
