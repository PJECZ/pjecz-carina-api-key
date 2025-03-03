"""
Exh Exhortos Archivos
"""

import hashlib
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.google_cloud_storage import upload_file_to_gcs
from ..dependencies.pwgen import generar_identificador
from ..models.exh_exhortos_archivos import ExhExhortoArchivo
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_archivos import (
    ExhExhortoArchivoFileDataAcuse,
    ExhExhortoArchivoFileDataArchivo,
    ExhExhortoArchivoOut,
    OneExhExhortoArchivoOut,
)
from ..settings import get_settings
from .exh_exhortos import get_exhorto_with_exhorto_origen_id

exh_exhortos_archivos = APIRouter(prefix="/api/v5/exh_exhortos")


@exh_exhortos_archivos.post("/recibir_archivo", response_model=OneExhExhortoArchivoOut)
async def recibir_exhorto_archivo_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    archivo: UploadFile = File(...),
    exhortoOrigenId: str = Form(...),
):
    """Recibir un archivo de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar que el nombre del archivo termine en pdf
    if not archivo.filename.lower().endswith(".pdf"):
        return OneExhExhortoArchivoOut(
            success=False,
            message="Tipo de archivo no permitido",
            errors=["El nombre del archivo no termina en PDF"],
            data=None,
        )

    # Consultar el exhorto
    try:
        exh_exhorto = get_exhorto_with_exhorto_origen_id(database, exhortoOrigenId)
    except (MyNotValidParamError, MyNotExistsError) as error:
        return OneExhExhortoArchivoOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Consultar los archivos del exhorto
    exh_exhortos_archivos_consulta = (
        database.query(ExhExhortoArchivo)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(es_respuesta=False)
        .filter_by(estatus="A")
        .order_by(ExhExhortoArchivo.id)
        .all()
    )

    # Buscar el archivo a partir del nombre del archivo
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_archivo = None
    for item in exh_exhortos_archivos_consulta:
        total_contador += 1
        if item.nombre_archivo == archivo.filename and item.estado == "PENDIENTE":
            exh_exhorto_archivo = item
        if item.estado == "PENDIENTE":
            pendientes_contador += 1
        else:
            recibidos_contador += 1

    # Si NO se encontró el archivo, entonces entregar un error
    if exh_exhorto_archivo is None:
        return OneExhExhortoArchivoOut(
            success=False,
            message="No se encontró el archivo",
            errors=["Al parecer el archivo ya fue recibido o no se declaró en el exhorto"],
            data=None,
        )

    # Determinar el tamaño del archivo
    archivo_pdf_tamanio = archivo.size

    # Validar que el archivo no exceda el tamaño máximo permitido de 10MB
    if archivo_pdf_tamanio > 10 * 1024 * 1024:
        return OneExhExhortoArchivoOut(
            success=False,
            message="El archivo excede el tamaño máximo permitido",
            errors=["El archivo no debe exceder los 10MB"],
            data=None,
        )

    # Cargar el archivo en memoria
    archivo_en_memoria = archivo.file.read()

    # Validar la integridad del archivo con SHA1
    if exh_exhorto_archivo.hash_sha1 is not None and exh_exhorto_archivo.hash_sha1 != "":
        hasher_sha1 = hashlib.sha1()
        hasher_sha1.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha1 != hasher_sha1.hexdigest():
            return OneExhExhortoArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA1"],
                data=None,
            )

    # Validar la integridad del archivo con SHA256
    if exh_exhorto_archivo.hash_sha256 is not None and exh_exhorto_archivo.hash_sha256 != "":
        hasher_sha256 = hashlib.sha256()
        hasher_sha256.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha256 != hasher_sha256.hexdigest():
            return OneExhExhortoArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA256"],
                data=None,
            )

    # Definir el nombre del archivo a subir a Google Storage
    archivo_pdf_nombre = f"{exhortoOrigenId}_{str(recibidos_contador + 1).zfill(4)}.pdf"

    # Definir la ruta para blob_name con la fecha actual
    fecha_hora_recepcion = datetime.now()
    year = fecha_hora_recepcion.strftime("%Y")
    month = fecha_hora_recepcion.strftime("%m")
    day = fecha_hora_recepcion.strftime("%d")
    blob_name = f"exh_exhortos_archivos/{year}/{month}/{day}/{archivo_pdf_nombre}"

    # Almacenar el archivo en Google Cloud Storage
    settings = get_settings()
    try:
        archivo_pdf_url = upload_file_to_gcs(
            bucket_name=settings.cloud_storage_deposito,
            blob_name=blob_name,
            content_type="application/pdf",
            data=archivo_en_memoria,
        )
    except MyAnyError as error:
        return OneExhExhortoArchivoOut(
            success=False,
            message="Hubo un error al subir el archivo al storage",
            errors=[str(error)],
            data=None,
        )

    # Actualizar el archivo en la base de datos
    exh_exhorto_archivo.estado = "RECIBIDO"
    exh_exhorto_archivo.fecha_hora_recepcion = fecha_hora_recepcion
    exh_exhorto_archivo.tamano = archivo_pdf_tamanio
    exh_exhorto_archivo.url = archivo_pdf_url
    database.add(exh_exhorto_archivo)
    database.commit()

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivoFileDataArchivo(
        nombreArchivo=exh_exhorto_archivo.nombre_archivo,
        tamaño=archivo_pdf_tamanio,
    )

    # Consultar la cantidad de archivos PENDIENTES
    exh_exhortos_archivos_pendientes_cantidad = (
        database.query(ExhExhortoArchivo)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(es_respuesta=False)
        .filter_by(estado="PENDIENTE")
        .filter_by(estatus="A")
        .order_by(ExhExhortoArchivo.id)
        .count()
    )

    # Si YA NO HAY PENDIENTES entonces ES EL ULTIMO ARCHIVO
    acuse = None  # Si aún faltan archivos, entonces el acuse es nulo
    if exh_exhortos_archivos_pendientes_cantidad == 0:
        # Cambiar el estado de exh_exhorto a RECIBIDO y se define el folio de seguimiento
        exh_exhorto.estado = "RECIBIDO"
        exh_exhorto.folio_seguimiento = generar_identificador()
        exh_exhorto.respuesta_fecha_hora_recepcion = fecha_hora_recepcion
        exh_exhorto.respuesta_municipio_turnado_id = 30  # Saltillo
        exh_exhorto.respuesta_area_turnado_id = None  # Como el área NO esta definida se responde con nulo
        exh_exhorto.respuesta_area_turnado_nombre = None  # Como el área NO esta definida se responde con nulo
        database.add(exh_exhorto)
        database.commit()
        # Y se va a elaborar el acuse
        acuse = ExhExhortoArchivoFileDataAcuse(
            exhortoOrigenId=exh_exhorto.exhorto_origen_id,
            folioSeguimiento=exh_exhorto.folio_seguimiento,
            fechaHoraRecepcion=exh_exhorto.respuesta_fecha_hora_recepcion.strftime("%Y-%m-%d %H:%M:%S"),
            municipioAreaRecibeId=exh_exhorto.respuesta_municipio_turnado_id,
            areaRecibeId=exh_exhorto.respuesta_area_turnado_id,
            areaRecibeNombre=exh_exhorto.respuesta_area_turnado_nombre,
            urlInfo="https://www.google.com.mx",
        )

    # Juntar los datos para la respuesta
    data = ExhExhortoArchivoOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoArchivoOut(success=True, message="Archivo recibido con éxito", errors=[], data=data)
