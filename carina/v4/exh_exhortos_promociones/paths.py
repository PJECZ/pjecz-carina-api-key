"""
Exh Exhortos Promociones v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_promociones.crud import get_exh_exhorto_promocion
from carina.v4.exh_exhortos_promociones.schemas import ExhExhortoPromocionOut, OneExhExhortoPromocionOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos_promociones = APIRouter(prefix="/v4/exh_exhortos_promociones", tags=["exh exhortos promociones"])


@exh_exhortos_promociones.get("/{exh_exhorto_promocion_id}", response_model=OneExhExhortoPromocionOut)
async def detalle_exh_exhorto_promocion(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_promocion_id: int,
):
    """Detalle de una promoción a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_promocion = get_exh_exhorto_promocion(database, exh_exhorto_promocion_id)
        data = ExhExhortoPromocionOut.model_validate(exh_exhorto_promocion)
    except MyAnyError as error:
        return OneExhExhortoPromocionOut(success=False, errors=[str(error)])
    return OneExhExhortoPromocionOut(success=True, data=data)
