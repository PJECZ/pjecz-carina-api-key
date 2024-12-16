"""
Exh Exhortos Promociones v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_promociones.crud import create_exh_exhorto_promocion
from carina.v4.exh_exhortos_promociones.schemas import ExhExhortoPromocionIn, ExhExhortoPromocionOut, OneExhExhortoPromocionOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos_promociones = APIRouter(prefix="/v4/exh_exhortos_promociones", tags=["exh exhortos promociones"])


@exh_exhortos_promociones.post("", response_model=OneExhExhortoPromocionOut)
async def recibir_exhorto_promocion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_promocion_in: ExhExhortoPromocionIn,
):
    """Recibir una promoción de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_promocion = create_exh_exhorto_promocion(database, exh_exhorto_promocion_in)
    except MyAnyError as error:
        return OneExhExhortoPromocionOut(
            success=False,
            message="Error al recibir la promoción del exhorto",
            errors=[str(error)],
            data=None,
        )
    data = ExhExhortoPromocionOut(
        folioSeguimiento=exh_exhorto_promocion.exh_exhorto.folio_seguimiento,
        folioOrigenPromocion=exh_exhorto_promocion.folio_origen_promocion,
        fechaHora=exh_exhorto_promocion.creado.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoPromocionOut(success=True, message="Promoción recibida con éxito", errors=[], data=data)
