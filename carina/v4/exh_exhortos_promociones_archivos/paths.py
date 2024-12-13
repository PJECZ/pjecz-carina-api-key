"""
Exh Exhortos Promociones Archivos v4, rutas (paths)
"""

import hashlib
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_archivos.schemas import ExhExhortoArchivo
from carina.v4.exh_exhortos_promociones.crud import (
    get_exh_exhorto_promocion_by_folio_origen_promocion,
    update_exh_exhorto_promocion,
)
from carina.v4.exh_exhortos_promociones_archivos.crud import (
    get_exh_exhortos_promociones_archivos,
    update_exh_exhorto_promocion_archivo,
)
from carina.v4.exh_exhortos_promociones_archivos.schemas import (
    ExhExhortoPromocionArchivoDataAcuse,
    ExhExhortoPromocionArchivoOut,
    OneExhExhortoPromocionArchivoOut,
)
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from config.settings import get_settings
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.google_cloud_storage import upload_file_to_gcs
from lib.pwgen import generar_identificador

exh_exhortos_promociones_archivos = APIRouter(prefix="/v4/exh_exhortos_promociones_archivos", tags=["exh exhortos promociones"])


@exh_exhortos_promociones_archivos.post("/upload", response_model=OneExhExhortoPromocionArchivoOut)
async def recibir_exhorto_promocion_archivo_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    folioSeguimiento: str,
    folioOrigenPromocion: str,
    archivo: UploadFile,
):
    """Recibir un archivo de una promoción"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar que el nombre del archivo termine en pdf
    if not archivo.filename.lower().endswith(".pdf"):
        return OneExhExhortoPromocionArchivoOut(
            success=False,
            message="Tipo de archivo no permitido",
            errors=["El nombre del archivo no termina en PDF"],
            data=None,
        )

    # Consultar y validar la promoción a partir de folioSeguimiento y folioOrigenPromocion
    try:
        exh_exhorto_promocion = get_exh_exhorto_promocion_by_folio_origen_promocion(
            database=database,
            folio_seguimiento=folioSeguimiento,
            folio_origen_promocion=folioOrigenPromocion,
        )
    except MyAnyError as error:
        return OneExhExhortoPromocionArchivoOut(
            success=False,
            message="No se encontró la promoción",
            errors=[str(error)],
            data=None,
        )

    # Consultar los archivos de la promoción y buscar el archivo que se pretende subir
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_promocion_archivo = None
    for item in get_exh_exhortos_promociones_archivos(database, exh_exhorto_promocion.id):
        total_contador += 1
        if item.nombre_archivo == archivo.filename and item.estado == "PENDIENTE":
            exh_exhorto_promocion_archivo = item
        if item.estado == "PENDIENTE":
            pendientes_contador += 1
        else:
            recibidos_contador += 1

    # Si NO se encontró el archivo, entonces entregar un error
    if exh_exhorto_promocion_archivo is None:
        return OneExhExhortoPromocionArchivoOut(
            success=False,
            message="No se encontró el archivo",
            errors=["Al parecer el archivo ya fue recibido o no se declaró en la promoción"],
            data=None,
        )

    # Determinar el tamaño del archivo
    archivo_pdf_tamanio = archivo.size

    # Validar que el archivo no exceda el tamaño máximo permitido de 10MB
    if archivo_pdf_tamanio > 10 * 1024 * 1024:
        return OneExhExhortoPromocionArchivoOut(
            success=False,
            message="El archivo excede el tamaño máximo permitido",
            errors=["El archivo no debe exceder los 10MB"],
            data=None,
        )

    # Cargar el archivo en memoria
    archivo_en_memoria = archivo.file.read()

    # Validar la integridad del archivo con SHA1
    if exh_exhorto_promocion_archivo.hash_sha1 != "":
        hasher_sha1 = hashlib.sha1()
        hasher_sha1.update(archivo_en_memoria)
        if exh_exhorto_promocion_archivo.hash_sha1 != hasher_sha1.hexdigest():
            return OneExhExhortoPromocionArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA1"],
                data=None,
            )

    # Validar la integridad del archivo con SHA256
    if exh_exhorto_promocion_archivo.hash_sha256 != "":
        hasher_sha256 = hashlib.sha256()
        hasher_sha256.update(archivo_en_memoria)
        if exh_exhorto_promocion_archivo.hash_sha256 != hasher_sha256.hexdigest():
            return OneExhExhortoPromocionArchivoOut(
                success=False,
                message="El archivo está corrupto",
                errors=["El archivo no coincide con el hash SHA256"],
                data=None,
            )

    # Definir el nombre del archivo a subir a Google Storage
    archivo_pdf_nombre = f"{folioOrigenPromocion}_{str(recibidos_contador + 1).zfill(4)}.pdf"

    # Definir la ruta para blob_name con la fecha actual
    fecha_hora_recepcion = datetime.now()
    year = fecha_hora_recepcion.strftime("%Y")
    month = fecha_hora_recepcion.strftime("%m")
    day = fecha_hora_recepcion.strftime("%d")
    blob_name = f"exh_exhortos_promociones_archivos/{year}/{month}/{day}/{archivo_pdf_nombre}"

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
        return OneExhExhortoPromocionArchivoOut(
            success=False,
            message="Hubo un error al subir el archivo al storage",
            errors=[str(error)],
            data=None,
        )

    # Cambiar el estado del archivo a RECIBIDO
    exh_exhorto_promocion_archivo = update_exh_exhorto_promocion_archivo(
        database=database,
        exh_exhorto_promocion_archivo=exh_exhorto_promocion_archivo,
        estado="RECIBIDO",
        fecha_hora_recepcion=fecha_hora_recepcion,
        tamano=archivo_pdf_tamanio,
        url=archivo_pdf_url,
    )

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivo(
        nombreArchivo=exh_exhorto_promocion_archivo.nombre_archivo,
        hashSha1=exh_exhorto_promocion_archivo.hash_sha1,
        hashSha256=exh_exhorto_promocion_archivo.hash_sha256,
        tipoDocumento=exh_exhorto_promocion_archivo.tipo_documento,
    )

    # Consultar los archivos PENDIENTES del exhorto
    exh_exhortos_promociones_archivos_pendientes = get_exh_exhortos_promociones_archivos(
        database=database,
        exh_exhorto_promocion_id=exh_exhorto_promocion.id,
        estado="PENDIENTE",
    )

    # Si YA NO HAY pendientes, entonces se manda contenido en el acuse
    if exh_exhortos_promociones_archivos_pendientes.count() == 0:
        # Entonces ES EL ÚLTIMO ARCHIVO, se cambia el estado de la promoción a RECIBIDO
        exh_exhorto_promocion_actualizado = update_exh_exhorto_promocion(
            database=database,
            exh_exhorto_promocion=exh_exhorto_promocion,
            estado="ENVIADO",
        )
        # Y se va a elaborar el acuse
        acuse = ExhExhortoPromocionArchivoDataAcuse(
            folioOrigenPromocion=exh_exhorto_promocion_actualizado.folio_origen_promocion,
            folioPromocionRecibida=generar_identificador(),  # TODO: Debe de conservarse en la base de datos
            fechaHoraRecepcion=datetime.now(),  # TODO: Debe de conservarse en la base de datos
        )
    else:
        # Aún faltan archivos, entonces el acuse no lleva contenido
        acuse = ExhExhortoPromocionArchivoDataAcuse(
            folioOrigenPromocion="",
            folioPromocionRecibida="",
            fechaHoraRecepcion=datetime.now(),
        )

    # Juntar los datos para la respuesta
    data = ExhExhortoPromocionArchivoOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoPromocionArchivoOut(success=True, message="Archivo recibido con éxito", errors=[], data=data)
