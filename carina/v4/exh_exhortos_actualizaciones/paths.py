"""
Exh Exhortos Actualizaciones v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_actualizaciones.crud import create_exh_exhorto_actualizacion
from carina.v4.exh_exhortos_actualizaciones.schemas import (
    ExhExhortoActualizacionIn,
    ExhExhortoActualizacionOut,
    OneExhExhortoActualizacionOut,
)
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos_actualizaciones = APIRouter(prefix="/v4/exh_exhortos_actualizaciones", tags=["exh exhortos actualizaciones"])


@exh_exhortos_actualizaciones.post("", response_model=OneExhExhortoActualizacionOut)
async def recibir_exhorto_actualizacion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_actualizacion_in: ExhExhortoActualizacionIn,
):
    """Recibir una actualización de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS ACTUALIZACIONES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_actualizacion = create_exh_exhorto_actualizacion(database, exh_exhorto_actualizacion_in)
    except MyAnyError as error:
        return OneExhExhortoActualizacionOut(
            success=False,
            message="Error al recibir la actualización",
            errors=[str(error)],
            data=None,
        )
    data = ExhExhortoActualizacionOut(
        exhortoId=exh_exhorto_actualizacion.exh_exhorto.exhorto_origen_id,
        actualizacionOrigenId=exh_exhorto_actualizacion.actualizacion_origen_id,
        fechaHora=exh_exhorto_actualizacion.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoActualizacionOut(success=True, message="Actualización recibida con éxito", errors=[], data=data)
