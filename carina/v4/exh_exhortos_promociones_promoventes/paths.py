"""
Exh Exhortos Promociones Promoventes v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_promociones_promoventes.crud import (
    get_exh_exhorto_promocion_promovente,
    get_exh_exhortos_promociones_promoventes,
)
from carina.v4.exh_exhortos_promociones_promoventes.schemas import (
    ExhExhortoPromocionPromoventeOut,
    OneExhExhortoPromocionPromoventeOut,
)
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos_promociones_promoventes = APIRouter(
    prefix="/v4/exh_exhortos_promociones_promoventes", tags=["exh exhortos promociones"]
)


@exh_exhortos_promociones_promoventes.get(
    "/{exh_exhorto_promocion_promovente_id}", response_model=OneExhExhortoPromocionPromoventeOut
)
async def detalle_exh_exhorto_promocion_provente(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_promocion_promovente_id: int,
):
    """Detalle de un promovente de una promoción a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES PROMOVENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_promocion_promovente = get_exh_exhorto_promocion_promovente(database, exh_exhorto_promocion_promovente_id)
        data = ExhExhortoPromocionPromoventeOut.model_validate(exh_exhorto_promocion_promovente)
    except MyAnyError as error:
        return OneExhExhortoPromocionPromoventeOut(success=False, errors=[str(error)])
    return OneExhExhortoPromocionPromoventeOut(success=True, data=data)
