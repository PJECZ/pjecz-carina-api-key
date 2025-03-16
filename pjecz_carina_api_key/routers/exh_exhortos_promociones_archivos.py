"""
Exh Exhortos Promociones Archivos
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
from ..models.exh_exhortos_promociones_archivos import ExhExhortoPromocionArchivo
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_promociones_archivos import (
    ExhExhortoPromocionArchivoDataAcuse,
    ExhExhortoPromocionArchivoDataArchivo,
    ExhExhortoPromocionArchivoOut,
    OneExhExhortoPromocionArchivoOut,
)
from ..settings import get_settings
from .exh_exhortos_promociones import get_exhorto_promocion

exh_exhortos_promociones_archivos = APIRouter(prefix="/api/v5/exh_exhortos")


@exh_exhortos_promociones_archivos.post("/recibir_promocion_archivo", response_model=OneExhExhortoPromocionArchivoOut)
async def recibir_exhorto_promocion_archivo_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    archivo: UploadFile = File(...),
    folioSeguimiento: str = Form(...),
    folioOrigenPromocion: str = Form(...),
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

    # Consultar la promoción
    try:
        exh_exhorto_promocion = get_exhorto_promocion(
            database=database,
            folio_seguimiento=folioSeguimiento,
            folio_origen_promocion=folioOrigenPromocion,
        )
    except (MyNotValidParamError, MyNotExistsError) as error:
        return OneExhExhortoPromocionArchivoOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Consultar los archivos de la promoción
    exh_exhortos_promociones_archivos_consulta = (
        database.query(ExhExhortoPromocionArchivo)
        .filter_by(exh_exhorto_promocion_id=exh_exhorto_promocion.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoPromocionArchivo.id)
        .all()
    )

    # Buscar el archivo que se pretende subir
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_promocion_archivo = None
    for item in exh_exhortos_promociones_archivos_consulta:
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
    if exh_exhorto_promocion_archivo.hash_sha1 is not None and exh_exhorto_promocion_archivo.hash_sha1 != "":
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
    if exh_exhorto_promocion_archivo.hash_sha256 is not None and exh_exhorto_promocion_archivo.hash_sha256 != "":
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

    # Actualizar el archivo en la base de datos
    exh_exhorto_promocion_archivo.estado = "RECIBIDO"
    exh_exhorto_promocion_archivo.fecha_hora_recepcion = fecha_hora_recepcion
    exh_exhorto_promocion_archivo.tamano = archivo_pdf_tamanio
    exh_exhorto_promocion_archivo.url = archivo_pdf_url
    database.add(exh_exhorto_promocion_archivo)
    database.commit()
    database.refresh(exh_exhorto_promocion_archivo)

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoPromocionArchivoDataArchivo(
        nombreArchivo=exh_exhorto_promocion_archivo.nombre_archivo,
        tamaño=exh_exhorto_promocion_archivo.tamano,
    )

    # Consultar la cantidad de archivos PENDIENTES de la promoción
    exh_exhortos_promociones_archivos_pendientes_cantidad = (
        database.query(ExhExhortoPromocionArchivo)
        .filter_by(exh_exhorto_promocion_id=exh_exhorto_promocion.id)
        .filter_by(estado="PENDIENTE")
        .filter_by(estatus="A")
        .order_by(ExhExhortoPromocionArchivo.id)
        .count()
    )

    # Si YA NO HAY PENDIENTES entonces ES EL ÚLTIMO ARCHIVO
    acuse = None
    if exh_exhortos_promociones_archivos_pendientes_cantidad == 0:
        # Actualizar la promoción
        exh_exhorto_promocion.folio_promocion_recibida = generar_identificador()
        exh_exhorto_promocion.estado = "ENVIADO"
        database.add(exh_exhorto_promocion)
        database.commit()
        # Elaborar el acuse
        acuse = ExhExhortoPromocionArchivoDataAcuse(
            folioOrigenPromocion=exh_exhorto_promocion.folio_origen_promocion,
            folioPromocionRecibida=exh_exhorto_promocion.folio_promocion_recibida,
            fechaHoraRecepcion=exh_exhorto_promocion.creado.strftime("%Y-%m-%d %H:%M:%S"),
        )

    # Juntar los datos para la respuesta
    data = ExhExhortoPromocionArchivoOut(
        archivo=archivo,
        acuse=acuse,
    )

    # Entregar la respuesta
    return OneExhExhortoPromocionArchivoOut(success=True, message="Archivo recibido con éxito", errors=[], data=data)
