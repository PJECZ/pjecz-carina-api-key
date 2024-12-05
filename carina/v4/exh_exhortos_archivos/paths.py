"""
Exh Exhortos Archivos v4, rutas (paths)
"""

import hashlib
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos.crud import get_exh_exhorto_by_exhorto_origen_id, update_exh_exhorto
from carina.v4.exh_exhortos_archivos.crud import get_exh_exhortos_archivos, update_exh_exhorto_archivo
from carina.v4.exh_exhortos_archivos.schemas import (
    ExhExhortoArchivoFileDataAcuseOut,
    ExhExhortoArchivoFileDataArchivo,
    ExhExhortoArchivoOut,
    ExhExhortoArchivoRespuestaDataAcuse,
    ExhExhortoArchivoRespuestaOut,
    OneExhExhortoArchivoOut,
    OneExhExhortoArchivoRespuestaOut,
)
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from config.settings import get_settings
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.google_cloud_storage import upload_file_to_gcs
from lib.pwgen import generar_identificador

exh_exhortos_archivos = APIRouter(prefix="/v4/exh_exhortos_archivos", tags=["exh exhortos archivos"])


@exh_exhortos_archivos.post("/responder_upload", response_model=OneExhExhortoArchivoRespuestaOut)
async def recibir_archivo_respuesta_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exhortoOrigenId: str,
    respuestaOrigenId: str,
    archivo: UploadFile,
):
    """Recibir un archivo de una respuesta"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar que el nombre del archivo termine en pdf
    if not archivo.filename.lower().endswith(".pdf"):
        return OneExhExhortoArchivoRespuestaOut(
            success=False,
            message="Tipo de archivo no permitido",
            errors=["El nombre del archivo no termina en PDF"],
        )

    # Consultar y validar el exhorto a partir del exhortoOrigenId
    try:
        exh_exhorto = get_exh_exhorto_by_exhorto_origen_id(database, exhortoOrigenId)
    except MyAnyError as error:
        return OneExhExhortoArchivoRespuestaOut(
            success=False,
            message="No se encontró el exhorto",
            errors=[str(error)],
        )

    # Consultar los archivos del exhorto y buscar el archivo a partir del nombre del archivo
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_archivo = None
    for item in get_exh_exhortos_archivos(database=database, exh_exhorto_id=exh_exhorto.id, es_respuesta=True).all():
        total_contador += 1
        if item.nombre_archivo == archivo.filename and item.estado == "PENDIENTE":
            exh_exhorto_archivo = item
        if item.estado == "PENDIENTE":
            pendientes_contador += 1
        else:
            recibidos_contador += 1

    # Si NO se encontró el archivo, entonces entregar un error
    if exh_exhorto_archivo is None:
        return OneExhExhortoArchivoRespuestaOut(
            success=False,
            message="No se encontró el archivo",
            errors=["Al parecer el archivo ya fue recibido o no se declaró en el exhorto"],
        )

    # Determinar el tamaño del archivo
    archivo_pdf_tamanio = archivo.size

    # Validar que el archivo no exceda el tamaño máximo permitido de 10MB
    if archivo_pdf_tamanio > 10 * 1024 * 1024:
        return OneExhExhortoArchivoRespuestaOut(
            success=False,
            message="El archivo excede el tamaño máximo permitido",
            errors=["El archivo no debe exceder los 10MB"],
        )

    # Cargar el archivo en memoria
    archivo_en_memoria = archivo.file.read()

    # Validar la integridad del archivo con SHA1
    if exh_exhorto_archivo.hash_sha1 != "":
        hasher_sha1 = hashlib.sha1()
        hasher_sha1.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha1 != hasher_sha1.hexdigest():
            return OneExhExhortoArchivoRespuestaOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA1"],
            )

    # Validar la integridad del archivo con SHA256
    if exh_exhorto_archivo.hash_sha256 != "":
        hasher_sha256 = hashlib.sha256()
        hasher_sha256.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha256 != hasher_sha256.hexdigest():
            return OneExhExhortoArchivoRespuestaOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA256"],
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
            message="Hubo un error nuestro al subir el archivo a Google Storage",
            errors=[str(error)],
        )

    # Cambiar el estado a RECIBIDO
    exh_exhorto_archivo = update_exh_exhorto_archivo(
        database=database,
        exh_exhorto_archivo=exh_exhorto_archivo,
        estado="RECIBIDO",
        url=archivo_pdf_url,
        tamano=archivo_pdf_tamanio,
        fecha_hora_recepcion=fecha_hora_recepcion,
    )

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivoFileDataArchivo(
        nombreArchivo=exh_exhorto_archivo.nombre_archivo,
        tamaño=archivo_pdf_tamanio,
    )

    # Definir el acuse
    acuse = ExhExhortoArchivoRespuestaDataAcuse(
        exhortoId=exhortoOrigenId,
        respuestaOrigenId=respuestaOrigenId,
        fechaHoraRecepcion=exh_exhorto.modificado,
    )

    # Definir el data
    data = ExhExhortoArchivoRespuestaOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoArchivoRespuestaOut(data=data)


@exh_exhortos_archivos.post("/upload", response_model=OneExhExhortoArchivoOut)
async def recibir_archivo_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exhortoOrigenId: str,
    archivo: UploadFile,
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
        )

    # Consultar y validar el exhorto a partir del exhortoOrigenId
    try:
        exh_exhorto = get_exh_exhorto_by_exhorto_origen_id(database, exhortoOrigenId)
    except MyAnyError as error:
        return OneExhExhortoArchivoOut(
            success=False,
            message="No se encontró el exhorto",
            errors=[str(error)],
        )

    # Consultar los archivos del exhorto y buscar el archivo a partir del nombre del archivo
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_archivo = None
    for item in get_exh_exhortos_archivos(database=database, exh_exhorto_id=exh_exhorto.id, es_respuesta=False).all():
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
        )

    # Determinar el tamaño del archivo
    archivo_pdf_tamanio = archivo.size

    # Validar que el archivo no exceda el tamaño máximo permitido de 10MB
    if archivo_pdf_tamanio > 10 * 1024 * 1024:
        return OneExhExhortoArchivoOut(
            success=False,
            message="El archivo excede el tamaño máximo permitido",
            errors=["El archivo no debe exceder los 10MB"],
        )

    # Cargar el archivo en memoria
    archivo_en_memoria = archivo.file.read()

    # Validar la integridad del archivo con SHA1
    if exh_exhorto_archivo.hash_sha1 != "":
        hasher_sha1 = hashlib.sha1()
        hasher_sha1.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha1 != hasher_sha1.hexdigest():
            return OneExhExhortoArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA1"],
            )

    # Validar la integridad del archivo con SHA256
    if exh_exhorto_archivo.hash_sha256 != "":
        hasher_sha256 = hashlib.sha256()
        hasher_sha256.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha256 != hasher_sha256.hexdigest():
            return OneExhExhortoArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA256"],
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
        )

    # Cambiar el estado del archivo a RECIBIDO
    exh_exhorto_archivo = update_exh_exhorto_archivo(
        database=database,
        exh_exhorto_archivo=exh_exhorto_archivo,
        estado="RECIBIDO",
        url=archivo_pdf_url,
        tamano=archivo_pdf_tamanio,
        fecha_hora_recepcion=fecha_hora_recepcion,
    )

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivoFileDataArchivo(
        nombreArchivo=exh_exhorto_archivo.nombre_archivo,
        tamaño=archivo_pdf_tamanio,
    )

    # Consultar los archivos PENDIENTES del exhorto
    exh_exhorto_archivos_pendientes = get_exh_exhortos_archivos(
        database=database,
        exh_exhorto_id=exh_exhorto.id,
        estado="PENDIENTE",
    )

    # Si YA NO HAY pendientes, entonces se manda contenido en el acuse
    if exh_exhorto_archivos_pendientes.count() == 0:
        # Entonces ES EL ULTIMO ARCHIVO, se cambia el estado de exh_exhorto a RECIBIDO y se define el folio de seguimiento
        exh_exhorto_actualizado = update_exh_exhorto(
            database=database,
            exh_exhorto=exh_exhorto,
            estado="RECIBIDO",
            folio_seguimiento=generar_identificador(),
        )
        # Y se va a elaborar el acuse
        acuse = ExhExhortoArchivoFileDataAcuseOut(
            exhortoOrigenId=exh_exhorto_actualizado.exhorto_origen_id,
            folioSeguimiento=exh_exhorto_actualizado.folio_seguimiento,
            fechaHoraRecepcion=exh_exhorto_actualizado.respuesta_fecha_hora_recepcion,
            municipioAreaRecibeId=exh_exhorto_actualizado.respuesta_municipio_turnado_id,
            areaRecibeId=exh_exhorto_actualizado.respuesta_area_turnado_id,
            areaRecibeNombre=exh_exhorto_actualizado.respuesta_area_turnado_nombre,
            urlInfo="https://www.google.com.mx",
        )
    else:
        # Aún faltan archivos, entonces el acuse no lleva contenido
        acuse = ExhExhortoArchivoFileDataAcuseOut(
            exhortoOrigenId=exh_exhorto.exhorto_origen_id,
            folioSeguimiento="",
            fechaHoraRecepcion=None,
            municipioAreaRecibeId=1,
            areaRecibeId="",
            areaRecibeNombre="",
            urlInfo="",
        )

    # Juntar los datos para la respuesta
    data = ExhExhortoArchivoOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoArchivoOut(success=True, data=data)
