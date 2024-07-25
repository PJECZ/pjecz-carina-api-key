"""
Exh Exhortos Archivos v4, rutas (paths)
"""

import hashlib
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos.crud import get_exh_exhorto_by_exhorto_origen_id, update_set_exhorto
from carina.v4.exh_exhortos_archivos.crud import get_exh_exhortos_archivos, update_set_exhorto_archivo
from carina.v4.exh_exhortos_archivos.schemas import (
    ExhExhortoArchivoFileDataAcuseOut,
    ExhExhortoArchivoFileDataArchivoOut,
    ExhExhortoArchivoFileDataOut,
    OneExhExhortoArchivoFileOut,
    OneExhExhortoArchivoRecibirRespuestaExhortoOut,
)
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from config.settings import get_settings
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.google_cloud_storage import upload_file_to_gcs
from lib.pwgen import generar_identificador

exh_exhortos_archivos = APIRouter(prefix="/v4/exh_exhortos_archivos", tags=["exhortos"])


@exh_exhortos_archivos.post("/upload/responder", response_model=OneExhExhortoArchivoRecibirRespuestaExhortoOut)
async def recibir_exhorto_archivo_respuesta_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    archivo: UploadFile,
):
    """Recibir un archivo de respuesta"""

    # TODO: Implementar la lógica de recibir un archivo de respuesta
    return OneExhExhortoArchivoRecibirRespuestaExhortoOut()


@exh_exhortos_archivos.post("/upload", response_model=OneExhExhortoArchivoFileOut)
async def recibir_exhorto_archivo_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exhortoOrigenId: str,
    archivo: UploadFile,
):
    """Recibir un archivo del exhorto"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar que el nombre del archivo termine en pdf
    if not archivo.filename.lower().endswith(".pdf"):
        return OneExhExhortoArchivoFileOut(
            success=False,
            message="Tipo de archivo no permitido",
            errors=["El nombre del archivo no termina en PDF"],
        )

    # Consultar y validar el exhorto a partir del exhortoOrigenId
    try:
        exh_exhorto = get_exh_exhorto_by_exhorto_origen_id(database, exhortoOrigenId)
    except MyAnyError as error:
        return OneExhExhortoArchivoFileOut(
            success=False,
            message="No se encontró el exhorto",
            errors=[str(error)],
        )

    # Consultar los archivos del exhorto y buscar el archivo a partir del nombre del archivo
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_archivo = False
    for item in get_exh_exhortos_archivos(database, exhortoOrigenId).all():
        total_contador += 1
        if item.nombre_archivo == archivo.filename and item.estado == "PENDIENTE":
            exh_exhorto_archivo = item
        if item.estado == "PENDIENTE":
            pendientes_contador += 1
        else:
            recibidos_contador += 1

    # Si NO se encontró el archivo, entonces entregar un error
    if exh_exhorto_archivo is False:
        return OneExhExhortoArchivoFileOut(
            success=False,
            message="No se encontró el archivo",
            errors=["Al parecer el archivo ya fue recibido o no se declaró en el exhorto"],
        )

    # Determinar el tamano del archivo
    archivo_pdf_tamanio = archivo.size

    # Validar que el archivo no execeda el tamaño máximo permitido de 10MB
    if archivo_pdf_tamanio > 10 * 1024 * 1024:
        return OneExhExhortoArchivoFileOut(
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
            return OneExhExhortoArchivoFileOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA1"],
            )

    # Validar la integridad del archivo con SHA256
    if exh_exhorto_archivo.hash_sha256 != "":
        hasher_sha256 = hashlib.sha256()
        hasher_sha256.update(archivo_en_memoria)
        if exh_exhorto_archivo.hash_sha256 != hasher_sha256.hexdigest():
            return OneExhExhortoArchivoFileOut(
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

    # Almacenar el archivo en Google Storage
    settings = get_settings()
    try:
        archivo_pdf_url = upload_file_to_gcs(
            bucket_name=settings.cloud_storage_deposito,
            blob_name=blob_name,
            content_type="application/pdf",
            data=archivo_en_memoria,
        )
    except MyAnyError as error:
        return OneExhExhortoArchivoFileOut(
            success=False,
            message="Hubo un error nuestro al subir el archivo a Google Storage",
            errors=[str(error)],
        )

    # Cambiar el estado de exh_exhorto_archivo_encontrado a RECIBIDO
    exh_exhorto_archivo = update_set_exhorto_archivo(
        database=database,
        exh_exhorto_archivo=exh_exhorto_archivo,
        estado="RECIBIDO",
        url=archivo_pdf_url,
        tamano=archivo_pdf_tamanio,
        fecha_hora_recepcion=fecha_hora_recepcion,
    )

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivoFileDataArchivoOut(
        nombreArchivo=exh_exhorto_archivo.nombre_archivo,
        tamaño=archivo_pdf_tamanio,
    )

    # Si pendientes_contador + 1 = total_contador
    if pendientes_contador + 1 >= total_contador:
        # Generar el folio_seguimiento
        folio_seguimiento = generar_identificador()
        # Entonces ES EL ULTIMO ARCHIVO, se cambia el estado de exh_exhorto a RECIBIDO
        exh_exhorto_actualizado = update_set_exhorto(
            database=database,
            exh_exhorto=exh_exhorto,
            estado="RECIBIDO",
            folio_seguimiento=folio_seguimiento,
        )
        # Y se va a elaborar el acuse
        acuse = ExhExhortoArchivoFileDataAcuseOut(
            exhortoOrigenId=str(exh_exhorto_actualizado.exhorto_origen_id),
            folioSeguimiento=folio_seguimiento,
            fechaHoraRecepcion=fecha_hora_recepcion,
            municipioAreaRecibeId=exh_exhorto_actualizado.municipio_destino_id,
            areaRecibeId=exh_exhorto_actualizado.exh_area.clave,
            areaRecibeNombre=exh_exhorto_actualizado.exh_area.nombre,
            urlInfo="https://www.google.com.mx",
        )
    else:
        # Definir el acuse VACIO, porque aun faltan archivos
        acuse = ExhExhortoArchivoFileDataAcuseOut(
            exhortoOrigenId="",
            folioSeguimiento="",
            fechaHoraRecepcion=None,
            municipioAreaRecibeId=1,
            areaRecibeId="",
            areaRecibeNombre="",
            urlInfo="",
        )

    # Juntar los datos para la respuesta
    data = ExhExhortoArchivoFileDataOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoArchivoFileOut(success=True, data=data)
