"""
Exh Exhortos Actualizaciones v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.safe_string import safe_string
from ..models.exh_exhortos_actualizaciones import ExhExhortoActualizacion
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_actualizaciones import (
    ExhExhortoActualizacionIn,
    ExhExhortoActualizacionOut,
    OneExhExhortoActualizacionOut,
)
from .exh_exhortos import get_exh_exhorto, get_exh_exhorto_by_exhorto_origen_id

exh_exhortos_actualizaciones = APIRouter(prefix="/v4/exh_exhortos_actualizaciones", tags=["exh exhortos actualizaciones"])


def get_exh_exhortos_actualizaciones(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar las actualizaciones de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoActualizacion)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoActualizacion.id)
    )


def get_exh_exhorto_actualizacion(database: Session, exh_exhorto_actualizacion_id: int) -> ExhExhortoActualizacion:
    """Consultar una actualización de un exhorto por su id"""
    exh_exhorto_actualizacion = database.query(ExhExhortoActualizacion).get(exh_exhorto_actualizacion_id)
    if exh_exhorto_actualizacion is None:
        raise MyNotExistsError("No existe esa actualización de exhorto")
    if exh_exhorto_actualizacion.estatus != "A":
        raise MyIsDeletedError("No es activa esa actualización de exhorto, está eliminada")
    return exh_exhorto_actualizacion


def create_exh_exhorto_actualizacion(
    database: Session,
    exh_exhorto_actualizacion_in: ExhExhortoActualizacionIn,
) -> ExhExhortoActualizacion:
    """Crear una actualización de un exhorto"""

    # Inicializar
    exh_exhorto_actualizacion = ExhExhortoActualizacion()

    # Consultar el exhorto
    exh_exhorto = get_exh_exhorto_by_exhorto_origen_id(database, exh_exhorto_actualizacion_in.exhortoId)

    # Definir las propiedades
    exh_exhorto_actualizacion.exh_exhorto_id = exh_exhorto.id
    exh_exhorto_actualizacion.actualizacion_origen_id = exh_exhorto_actualizacion_in.actualizacionOrigenId
    exh_exhorto_actualizacion.tipo_actualizacion = exh_exhorto_actualizacion_in.tipoActualizacion
    try:
        exh_exhorto_actualizacion.fecha_hora = datetime.strptime(exh_exhorto_actualizacion_in.fechaHora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise MyNotValidParamError("La fecha y hora no tiene el formato correcto")
    exh_exhorto_actualizacion.descripcion = safe_string(exh_exhorto_actualizacion_in.descripcion, save_enie=True)
    exh_exhorto_actualizacion.remitente = "EXTERNO"

    # Insertar
    database.add(exh_exhorto_actualizacion)
    database.commit()
    database.refresh(exh_exhorto_actualizacion)

    # Entregar
    return exh_exhorto_actualizacion


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
