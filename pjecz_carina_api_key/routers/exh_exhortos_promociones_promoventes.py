"""
Exh Exhortos Promociones Promoventes v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromovente  # Es necesario...
from ..models.permisos import Permiso
from .exh_exhortos_promociones import get_exh_exhorto_promocion

exh_exhortos_promociones_promoventes = APIRouter(
    prefix="/v4/exh_exhortos_promociones_promoventes",
    tags=["exh exhortos promociones"],
)


def get_exh_exhortos_promociones_promoventes(database: Session, exh_exhorto_promocion_id: int) -> Any:
    """Consultar los promoventes de una promoción de un exhorto"""
    exh_exhorto_promocion = get_exh_exhorto_promocion(database, exh_exhorto_promocion_id)
    return (
        database.query(ExhExhortoPromocionPromovente)
        .filter_by(exh_exhorto_promocion_id=exh_exhorto_promocion.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoPromocionPromovente.id)
    )


def get_exh_exhorto_promocion_promovente(
    database: Session, exh_exhorto_promocion_promovente_id: int
) -> ExhExhortoPromocionPromovente:
    """Consultar un promovente de una promoción de un exhorto por su id"""
    exh_exhorto_promocion_promovente = database.query(ExhExhortoPromocionPromovente).get(exh_exhorto_promocion_promovente_id)
    if exh_exhorto_promocion_promovente is None:
        raise MyNotExistsError("No existe ese promovente de promoción de exhorto")
    if exh_exhorto_promocion_promovente.estatus != "A":
        raise MyIsDeletedError("No es activo ese promovente de promoción de exhorto, está eliminado")
    return exh_exhorto_promocion_promovente


@exh_exhortos_promociones_promoventes.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES PROMOVENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
