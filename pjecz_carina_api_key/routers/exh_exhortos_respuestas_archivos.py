"""
Exh Exhortos Respuestas Archivos, routers
"""

import hashlib
from datetime import datetime
from typing import Annotated

import pytz
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.google_cloud_storage import upload_file_to_gcs
from ..dependencies.pwgen import generar_identificador
from ..models.exh_exhortos_respuestas_archivos import ExhExhortoRespuestaArchivo
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_respuestas_archivos import (
    ExhExhortoRespuestaArchivoDataAcuse,
    ExhExhortoRespuestaArchivoDataArchivo,
    ExhExhortoRespuestaArchivoOut,
    OneExhExhortoRespuestaArchivoOut,
)
from ..settings import Settings, get_settings
from .exh_exhortos_respuestas import get_exhorto_respuesta

exh_exhortos_respuestas_archivos = APIRouter(prefix="/api/v5/exh_exhortos")


@exh_exhortos_respuestas_archivos.post("/recibir_respuesta_archivo", response_model=OneExhExhortoRespuestaArchivoOut)
async def recibir_exhorto_respuesta_archivo_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    archivo: UploadFile = File(...),
    exhortoId: str = Form(...),
    respuestaOrigenId: str = Form(...),
):
    """Recibir un archivo de una respuesta"""
    if current_user.permissions.get("EXH EXHORTOS RESPUESTAS ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar que el nombre del archivo termine en pdf
    if not archivo.filename.lower().endswith(".pdf"):
        return OneExhExhortoRespuestaArchivoOut(
            success=False,
            message="Tipo de archivo no permitido",
            errors=["El nombre del archivo no termina en PDF"],
            data=None,
        )

    # Consultar la respuesta
    try:
        exh_exhorto_respuesta = get_exhorto_respuesta(
            database=database,
            exhorto_id=exhortoId,
            respuesta_origen_id=respuestaOrigenId,
        )
    except (MyNotValidParamError, MyNotExistsError) as error:
        return OneExhExhortoRespuestaArchivoOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Consultar los archivos de la respuesta
    exh_exhortos_respuestas_archivos_consulta = (
        database.query(ExhExhortoRespuestaArchivo)
        .filter_by(exh_exhorto_respuesta_id=exh_exhorto_respuesta.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoRespuestaArchivo.id)
        .all()
    )

    # Buscar el archivo que se pretende subir
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_respuesta_archivo = None
    for item in exh_exhortos_respuestas_archivos_consulta:
        total_contador += 1
        if item.nombre_archivo == archivo.filename and item.estado == "PENDIENTE":
            exh_exhorto_respuesta_archivo = item
        if item.estado == "PENDIENTE":
            pendientes_contador += 1
        else:
            recibidos_contador += 1

    # Si NO se encontró el archivo, entonces entregar un error
    if exh_exhorto_respuesta_archivo is None:
        return OneExhExhortoRespuestaArchivoOut(
            success=False,
            message="No se encontró el archivo",
            errors=["Al parecer el archivo ya fue recibido o no se declaró en la respuesta"],
            data=None,
        )

    # Determinar el tamaño del archivo
    archivo_pdf_tamanio = archivo.size

    # Validar que el archivo no exceda el tamaño máximo permitido de 10MB
    if archivo_pdf_tamanio > 10 * 1024 * 1024:
        return OneExhExhortoRespuestaArchivoOut(
            success=False,
            message="El archivo excede el tamaño máximo permitido",
            errors=["El archivo no debe exceder los 10MB"],
            data=None,
        )

    # Cargar el archivo en memoria
    archivo_en_memoria = archivo.file.read()

    # Validar la integridad del archivo con SHA1
    if exh_exhorto_respuesta_archivo.hash_sha1 is not None and exh_exhorto_respuesta_archivo.hash_sha1 != "":
        hasher_sha1 = hashlib.sha1()
        hasher_sha1.update(archivo_en_memoria)
        if exh_exhorto_respuesta_archivo.hash_sha1 != hasher_sha1.hexdigest():
            return OneExhExhortoRespuestaArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA1"],
                data=None,
            )

    # Validar la integridad del archivo con SHA256
    if exh_exhorto_respuesta_archivo.hash_sha256 is not None and exh_exhorto_respuesta_archivo.hash_sha256 != "":
        hasher_sha256 = hashlib.sha256()
        hasher_sha256.update(archivo_en_memoria)
        if exh_exhorto_respuesta_archivo.hash_sha256 != hasher_sha256.hexdigest():
            return OneExhExhortoRespuestaArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA256"],
                data=None,
            )

    # Definir el nombre del archivo a subir a Google Storage
    archivo_pdf_nombre = f"{respuestaOrigenId}_{str(recibidos_contador + 1).zfill(4)}.pdf"

    # Definir la ruta para blob_name con la fecha actual
    fecha_hora_recepcion = datetime.now()
    year = fecha_hora_recepcion.strftime("%Y")
    month = fecha_hora_recepcion.strftime("%m")
    day = fecha_hora_recepcion.strftime("%d")
    blob_name = f"exh_exhortos_respuestas_archivos/{year}/{month}/{day}/{archivo_pdf_nombre}"

    # Almacenar el archivo en Google Cloud Storage
    try:
        archivo_pdf_url = upload_file_to_gcs(
            bucket_name=settings.cloud_storage_deposito,
            blob_name=blob_name,
            content_type="application/pdf",
            data=archivo_en_memoria,
        )
    except MyAnyError as error:
        return OneExhExhortoRespuestaArchivoOut(
            success=False,
            message="Hubo un error al subir el archivo al storage",
            errors=[str(error)],
            data=None,
        )

    # Actualizar el archivo en la base de datos
    exh_exhorto_respuesta_archivo.estado = "RECIBIDO"
    exh_exhorto_respuesta_archivo.fecha_hora_recepcion = fecha_hora_recepcion
    exh_exhorto_respuesta_archivo.tamano = archivo_pdf_tamanio
    exh_exhorto_respuesta_archivo.url = archivo_pdf_url
    database.add(exh_exhorto_respuesta_archivo)
    database.commit()
    database.refresh(exh_exhorto_respuesta_archivo)

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoRespuestaArchivoDataArchivo(
        nombreArchivo=exh_exhorto_respuesta_archivo.nombre_archivo,
        tamaño=exh_exhorto_respuesta_archivo.tamano,
    )

    # Consultar la cantidad de archivos PENDIENTES de la respuesta
    exh_exhortos_repuestas_archivos_pendientes_cantidad = (
        database.query(ExhExhortoRespuestaArchivo)
        .filter_by(exh_exhorto_respuesta_id=exh_exhorto_respuesta.id)
        .filter_by(estado="PENDIENTE")
        .filter_by(estatus="A")
        .order_by(ExhExhortoRespuestaArchivo.id)
        .count()
    )

    # Si YA NO HAY PENDIENTES entonces ES EL ÚLTIMO ARCHIVO
    acuse = None
    if exh_exhortos_repuestas_archivos_pendientes_cantidad == 0:
        # Actualizar la respuesta
        exh_exhorto_respuesta.folio_respuesta_recibida = generar_identificador()
        exh_exhorto_respuesta.estado = "ENVIADO"
        database.add(exh_exhorto_respuesta)
        database.commit()
        # Cambiar fecha_hora_recepcion de UTC a tiempo local
        utc_tz = pytz.utc
        local_tz = pytz.timezone(settings.tz)
        fecha_hora_recepcion = exh_exhorto_respuesta.creado.replace(tzinfo=utc_tz).astimezone(local_tz)
        # Elaborar el acuse
        acuse = ExhExhortoRespuestaArchivoDataAcuse(
            exhortoId=exh_exhorto_respuesta.exh_exhorto.exhorto_origen_id,
            respuestaOrigenId=exh_exhorto_respuesta.respuesta_origen_id,
            fechaHoraRecepcion=fecha_hora_recepcion.strftime("%Y-%m-%d %H:%M:%S"),
        )

    # Juntar los datos para la respuesta
    data = ExhExhortoRespuestaArchivoOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoRespuestaArchivoOut(success=True, message="Archivo recibido con éxito", errors=[], data=data)
