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

exh_exhortos_actualizaciones = APIRouter(prefix="/api/v5/exh_exhortos")


@exh_exhortos_actualizaciones.post("/actualizar", response_model=OneExhExhortoActualizacionOut)
async def recibir_exhorto_actualizacion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_actualizacion_in: ExhExhortoActualizacionIn,
):
    """Recibir una actualización de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS ACTUALIZACIONES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Inicializar listado de errores
    errores = []

    # Consultar el exhorto
    exh_exhorto = None
    try:
        exh_exhorto = get_exhorto_with_exhorto_origen_id(database, exh_exhorto_actualizacion_in.exhortoId)
    except MyAnyError as error:
        errores.append(str(error))

    # Validar actualizacionOrigenId
    actualizacion_origen_id = safe_string(exh_exhorto_actualizacion_in.actualizacionOrigenId, max_len=64, to_uppercase=False)
    if actualizacion_origen_id == "":
        errores.append("No es válido actualizacionOrigenId")

    # Validar tipoActualizacion
    tipo_actualizacion = safe_string(exh_exhorto_actualizacion_in.tipoActualizacion, max_len=64, to_uppercase=False)
    if tipo_actualizacion == "":
        errores.append("No es válido tipoActualizacion")

    # Validar la fecha_hora
    fecha_hora = None
    try:
        fecha_hora = datetime.strptime(exh_exhorto_actualizacion_in.fechaHora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        errores.append("No es válido fecha_hora")

    # Validar descripción
    descripcion = safe_string(exh_exhorto_actualizacion_in.descripcion, max_len=256, save_enie=True)
    if tipo_actualizacion == "":
        errores.append("No es válida la descripción")

    # Si hubo errores, se termina de forma fallida
    if len(errores) > 0:
        return OneExhExhortoActualizacionOut(
            success=False, message="Falló la recepción de la actualización", errors=errores, data=None
        )

    # Insertar la actualización
    exh_exhorto_actualizacion = ExhExhortoActualizacion(
        exh_exhorto_id=exh_exhorto.id,
        actualizacion_origen_id=actualizacion_origen_id,
        tipo_actualizacion=tipo_actualizacion,
        fecha_hora=fecha_hora,
        descripcion=descripcion,
        remitente="EXTERNO",
        estado="ENVIADO",
    )
    database.add(exh_exhorto_actualizacion)
    database.commit()
    database.refresh(exh_exhorto_actualizacion)

    # Entregar
    data = ExhExhortoActualizacionOut(
        exhortoId=exh_exhorto_actualizacion.exh_exhorto.exhorto_origen_id,
        actualizacionOrigenId=exh_exhorto_actualizacion.actualizacion_origen_id,
        fechaHora=exh_exhorto_actualizacion.creado.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoActualizacionOut(success=True, message="Actualización recibida con éxito", errors=[], data=data)
