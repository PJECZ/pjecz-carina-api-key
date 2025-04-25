"""
Exh Exhortos Respuestas, routers
"""

from datetime import datetime
from typing import Annotated

import pytz
from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.safe_string import safe_string
from ..models.exh_exhortos import ExhExhorto
from ..models.exh_exhortos_respuestas import ExhExhortoRespuesta
from ..models.exh_exhortos_respuestas_archivos import ExhExhortoRespuestaArchivo
from ..models.exh_exhortos_respuestas_videos import ExhExhortoRespuestaVideo
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_respuestas import ExhExhortoRespuestaIn, ExhExhortoRespuestaOut, OneExhExhortoRespuestaOut
from ..settings import Settings, get_settings
from .exh_exhortos import get_exhorto_with_exhorto_origen_id

exh_exhortos_respuestas = APIRouter(prefix="/api/v5/exh_exhortos")


def get_exhorto_respuesta(
    database: Annotated[Session, Depends(get_db)],
    exhorto_id: str,
    respuesta_origen_id: str,
) -> ExhExhortoRespuesta:
    """Consultar una respuesta con el folio de seguimiento del exhorto y origen ID de la respuesta."""

    # Validar exhorto_id
    exhorto_id = safe_string(exhorto_id, max_len=64, do_unidecode=True, to_uppercase=False)
    if exhorto_id == "":
        raise MyNotValidParamError("No es un 'exhorto id' válido")

    # Validar respuesta_origen_id
    respuesta_origen_id = safe_string(respuesta_origen_id, max_len=64, do_unidecode=True, to_uppercase=False)
    if respuesta_origen_id == "":
        raise MyNotValidParamError("No es una 'respuesta origen id' válida")

    # Consultar la promoción
    exh_exhorto_respuesta = (
        database.query(ExhExhortoRespuesta)
        .join(ExhExhorto)
        .filter(ExhExhorto.exhorto_origen_id == exhorto_id)
        .filter(ExhExhortoRespuesta.respuesta_origen_id == respuesta_origen_id)
        .filter(ExhExhortoRespuesta.estatus == "A")
        .first()
    )

    # Verificar que exista
    if exh_exhorto_respuesta is None:
        raise MyNotExistsError("No existe esa promoción de exhorto")

    # Entregar
    return exh_exhorto_respuesta


@exh_exhortos_respuestas.post("/recibir_respuesta", response_model=OneExhExhortoRespuestaOut)
async def recibir_exhorto_respuesta_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    exh_exhorto_respuesta_in: ExhExhortoRespuestaIn,
):
    """Recibir una respuesta de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS RESPUESTAS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Preparar las zonas horarias UTC y local
    utc_tz = pytz.utc
    local_tz = pytz.timezone(settings.tz)

    # Inicializar listado de errores
    errores = []

    # Consultar el exhorto
    exh_exhorto = None
    try:
        exh_exhorto = get_exhorto_with_exhorto_origen_id(database, exh_exhorto_respuesta_in.exhortoId)
    except MyAnyError as error:
        errores.append(str(error))

    # Validar respuestaOrigenId, obligatorio
    respuesta_origen_id = safe_string(
        exh_exhorto_respuesta_in.respuestaOrigenId, max_len=64, do_unidecode=True, to_uppercase=False
    )
    if respuesta_origen_id == "":
        errores.append("No es válido respuestaOrigenId")

    # TODO: Validar municipioTurnadoId, entero obligatorio es identificador INEGI
    municipio_turnado_id = exh_exhorto_respuesta_in.municipioTurnadoId

    # Validar areaTurnadoId, es opcional
    area_turnado_id = None
    if exh_exhorto_respuesta_in.areaTurnadoId is not None:
        area_turnado_id = safe_string(exh_exhorto_respuesta_in.areaTurnadoId)

    # Validar areaTurnadoNombre, obligatorio
    area_turnado_nombre = safe_string(exh_exhorto_respuesta_in.areaTurnadoNombre)
    if area_turnado_nombre == "":
        errores.append("No es válido areaTurnadoNombre")

    # Validar numeroExhorto, es opcional
    numero_exhorto = None
    if exh_exhorto_respuesta_in.numeroExhorto is not None:
        numero_exhorto = safe_string(exh_exhorto_respuesta_in.numeroExhorto)

    # Validar tipoDiligenciado, debe ser entero 0, 1 o 2
    tipo_diligenciado = None
    if exh_exhorto_respuesta_in.tipoDiligenciado is not None:
        if exh_exhorto_respuesta_in.tipoDiligenciado in (0, 1, 2):
            tipo_diligenciado = exh_exhorto_respuesta_in.tipoDiligenciado
        else:
            errores.append("No es válido tipoDiligenciado")

    # Validar observaciones, es opcional
    observaciones = None
    if exh_exhorto_respuesta_in.observaciones is not None:
        observaciones = safe_string(exh_exhorto_respuesta_in.observaciones, save_enie=True, max_len=1000)

    # Si hubo errores, se termina de forma fallida
    if len(errores) > 0:
        return OneExhExhortoRespuestaOut(success=False, message="Falló la recepción de la respuesta", errors=errores, data=None)

    # Insertar la respuesta
    exh_exhorto_respuesta = ExhExhortoRespuesta(
        exh_exhorto_id=exh_exhorto.id,
        respuesta_origen_id=respuesta_origen_id,
        municipio_turnado_id=municipio_turnado_id,
        area_turnado_id=area_turnado_id,
        area_turnado_nombre=area_turnado_nombre,
        numero_exhorto=numero_exhorto,
        tipo_diligenciado=tipo_diligenciado,
        observaciones=observaciones,
        remitente="EXTERNO",
        estado="PENDIENTE",
    )
    database.add(exh_exhorto_respuesta)
    database.commit()
    database.refresh(exh_exhorto_respuesta)

    # El estado del exhorto cambia a RESPONDIDO
    exh_exhorto.estado = "RESPONDIDO"
    database.add(exh_exhorto)
    database.commit()

    # Insertar los archivos
    for archivo in exh_exhorto_respuesta_in.archivos:
        exh_exhorto_respuesta_archivo = ExhExhortoRespuestaArchivo(
            exh_exhorto_respuesta_id=exh_exhorto_respuesta.id,
            nombre_archivo=archivo.nombreArchivo,
            hash_sha1=archivo.hashSha1,
            hash_sha256=archivo.hashSha256,
            tipo_documento=archivo.tipoDocumento,
            estado="PENDIENTE",
            tamano=0,
            fecha_hora_recepcion=datetime.now(),
        )
        database.add(exh_exhorto_respuesta_archivo)

    # Insertar los videos
    for video in exh_exhorto_respuesta_in.videos:
        fecha = None
        try:
            if video.fecha is not None:
                fecha = datetime.strptime(video.fecha, "%Y-%m-%d")
        except ValueError:
            fecha = None
        exh_exhorto_video = ExhExhortoRespuestaVideo(
            exh_exhorto_respuesta=exh_exhorto_respuesta,
            titulo=safe_string(video.titulo, save_enie=True),
            descripcion=safe_string(video.descripcion, save_enie=True),
            fecha=fecha,
            url_acceso=video.urlAcceso,
        )
        database.add(exh_exhorto_video)

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto)

    # Cambiar fecha_hora de UTC a tiempo local
    fecha_hora = exh_exhorto_respuesta.creado.replace(tzinfo=utc_tz).astimezone(local_tz)

    # Entregar
    data = ExhExhortoRespuestaOut(
        exhortoId=exh_exhorto.exhorto_origen_id,
        respuestaOrigenId=exh_exhorto_respuesta.respuesta_origen_id,
        fechaHora=fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoRespuestaOut(success=True, message="Respuesta recibida con éxito", errors=[], data=data)
