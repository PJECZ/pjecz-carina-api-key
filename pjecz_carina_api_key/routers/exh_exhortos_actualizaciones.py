"""
Exh Exhortos Actualizaciones
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError
from ..dependencies.safe_string import safe_string
from ..models.exh_exhortos_actualizaciones import ExhExhortoActualizacion
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_actualizaciones import (
    ExhExhortoActualizacionIn,
    ExhExhortoActualizacionOut,
    OneExhExhortoActualizacionOut,
)
from .exh_exhortos import get_exhorto_with_exhorto_origen_id

exh_exhortos_actualizaciones = APIRouter(prefix="/api/v5/exh_exhortos_actualizaciones")


@exh_exhortos_actualizaciones.post("", response_model=OneExhExhortoActualizacionOut)
async def recibir_exhorto_actualizacion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_actualizacion_in: ExhExhortoActualizacionIn,
):
    """Recibir una actualización de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS ACTUALIZACIONES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Consultar el exhorto
    try:
        exh_exhorto = get_exhorto_with_exhorto_origen_id(database, exh_exhorto_actualizacion_in.exhortoId)
    except MyAnyError as error:
        return OneExhExhortoActualizacionOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Validar actualizacionOrigenId
    actualizacion_origen_id = safe_string(
        exh_exhorto_actualizacion_in.actualizacionOrigenId,
        max_len=48,
        do_unidecode=True,
        to_uppercase=False,
    )
    if actualizacion_origen_id == "":
        error = "No es un actualizacionOrigenId válido"
        return OneExhExhortoActualizacionOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Validar la fecha_hora
    try:
        fecha_hora = datetime.strptime(exh_exhorto_actualizacion_in.fechaHora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        error = "La fecha y hora no tiene el formato correcto"
        return OneExhExhortoActualizacionOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Insertar la actualización
    exh_exhorto_actualizacion = ExhExhortoActualizacion(
        exh_exhorto_id=exh_exhorto.id,
        actualizacion_origen_id=actualizacion_origen_id,
        tipo_actualizacion=safe_string(exh_exhorto_actualizacion_in.tipoActualizacion, max_len=48),
        fecha_hora=fecha_hora,
        descripcion=safe_string(exh_exhorto_actualizacion_in.descripcion, save_enie=True),
        remitente="EXTERNO",
    )
    database.add(exh_exhorto_actualizacion)
    database.commit()
    database.refresh(exh_exhorto_actualizacion)

    # Entregar
    data = ExhExhortoActualizacionOut(
        exhortoId=exh_exhorto_actualizacion.exh_exhorto.exhorto_origen_id,
        actualizacionOrigenId=exh_exhorto_actualizacion.actualizacion_origen_id,
        fechaHora=exh_exhorto_actualizacion.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoActualizacionOut(success=True, message="Actualización recibida con éxito", errors=[], data=data)
