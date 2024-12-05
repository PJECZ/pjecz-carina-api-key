"""
Exh Exhortos Actualizaciones v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_actualizaciones.crud import get_exh_exhorto_actualizacion
from carina.v4.exh_exhortos_actualizaciones.schemas import ExhExhortoActualizacionOut, OneExhExhortoActualizacionOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos_actualizaciones = APIRouter(prefix="/v4/exh_exhortos_actualizaciones", tags=["exh exhortos actualizaciones"])


@exh_exhortos_actualizaciones.get("/{exh_exhorto_actualizacion_id}")
async def consultar_exhorto_actualizacion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_actualizacion_id: int,
):
    """Consulta de una actualización de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS ACTUALIZACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_actualizacion = get_exh_exhorto_actualizacion(database, exh_exhorto_actualizacion_id)
        data = ExhExhortoActualizacionOut.model_validate(exh_exhorto_actualizacion)
    except MyAnyError as error:
        return OneExhExhortoActualizacionOut(success=False, errors=[str(error)])
    return OneExhExhortoActualizacionOut(success=True, data=data)
