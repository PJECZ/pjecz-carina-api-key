"""
Exh Exhortos Archivos v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi_pagination.ext.sqlalchemy import paginate

from config.settings import get_settings
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from lib.google_cloud_storage import upload_file_to_gcs

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos.crud import get_exh_exhorto, update_set_exhorto
from carina.v4.exh_exhortos_archivos.crud import get_exh_exhortos_archivos, get_exh_exhorto_archivo, update_set_exhorto_archivo
from carina.v4.exh_exhortos_archivos.schemas import (
    ExhExhortoArchivoFileDataAcuseOut,
    ExhExhortoArchivoFileDataArchivoOut,
    ExhExhortoArchivoFileDataOut,
    ExhExhortoArchivoFileOut,
    ExhExhortoArchivoOut,
    OneExhExhortoArchivoOut,
)
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user

exh_exhortos_archivos = APIRouter(prefix="/v4/exh_exhortos_archivos", tags=["exhortos"])


@exh_exhortos_archivos.get("", response_model=CustomPage[ExhExhortoArchivoOut])
async def paginado_exh_exhortos_archivos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de archivos de exhortos"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_exh_exhortos_archivos(database)
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@exh_exhortos_archivos.get("/{exh_exhorto_archivo_id}", response_model=OneExhExhortoArchivoOut)
async def detalle_exh_exhorto_archivo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_archivo_id: int,
):
    """Detalle de una archivo a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_archivo = get_exh_exhorto_archivo(database, exh_exhorto_archivo_id)
    except MyAnyError as error:
        return OneExhExhortoArchivoOut(success=False, errors=[str(error)])
    return OneExhExhortoArchivoOut(success=True, data=exh_exhorto_archivo)


@exh_exhortos_archivos.post("/upload")
async def upload_exh_exhorto_archivo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exhortoOrigenId: str,
    archivo: UploadFile,
):
    """Recibir un archivo"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar que el nombre del archivo termine en pdf
    if not archivo.filename.lower().endswith(".pdf"):
        return ExhExhortoArchivoFileOut(success=False, errors=["El archivo debe ser un PDF"])

    # Consultar y validar el exhorto a partir del exhortoOrigenId
    try:
        exh_exhorto = get_exh_exhorto(database, exhortoOrigenId)
    except MyAnyError as error:
        return ExhExhortoArchivoFileOut(success=False, errors=[str(error)])

    # Consultar los archivos del exhorto y buscar el archivo a partir del nombre del archivo
    total_contador = 0
    pendientes_contador = 0
    recibidos_contador = 0
    exh_exhorto_archivo_encontrado = False
    for exh_exhorto_archivo in get_exh_exhortos_archivos(database, exhortoOrigenId).all():
        total_contador += 1
        if exh_exhorto_archivo.nombre_archivo == archivo.filename and exh_exhorto_archivo.estado == "PENDIENTE":
            exh_exhorto_archivo_encontrado = exh_exhorto_archivo
        if exh_exhorto_archivo.estado == "PENDIENTE":
            pendientes_contador += 1
        else:
            recibidos_contador += 1

    # Si NO se encontró el archivo, entonces entregar un error
    if exh_exhorto_archivo_encontrado is False:
        return ExhExhortoArchivoFileOut(success=False, errors=["No se encontró el archivo"])

    # TODO: Validar la integridad del archivo con los hashes

    # Definir el nombre del archivo a subir a Google Storage
    archivo_pdf_nombre = f"{exhortoOrigenId}_{str(recibidos_contador + 1).zfill(4)}.pdf"

    # Definir la ruta para blob_name con la fecha actual
    fecha_hora_recepcion = datetime.now()
    year = fecha_hora_recepcion.strftime("%Y")
    month = fecha_hora_recepcion.strftime("%m")
    day = fecha_hora_recepcion.strftime("%d")
    blob_name = f"exh_exhortos_archivos/{year}/{month}/{day}/{archivo_pdf_nombre}"

    # Determinar el tamano del archivo
    archivo_pdf_tamanio = archivo.size

    # Almacenar el archivo en Google Storage
    settings = get_settings()
    try:
        archivo_pdf_url = upload_file_to_gcs(
            bucket_name=settings.cloud_storage_deposito,
            blob_name=blob_name,
            content_type="application/pdf",
            data=archivo.file,
        )
    except MyAnyError as error:
        return ExhExhortoArchivoFileOut(success=False, errors=[str(error)])

    # Cambiar el estado de exh_exhorto_archivo_encontrado a RECIBIDO
    exh_exhorto_archivo_encontrado = update_set_exhorto_archivo(
        database=database,
        exh_exhorto_archivo=exh_exhorto_archivo_encontrado,
        estado="RECIBIDO",
        url=archivo_pdf_url,
        tamano=archivo_pdf_tamanio,
        fecha_hora_recepcion=fecha_hora_recepcion,
    )

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivoFileDataArchivoOut(
        nombreArchivo=exh_exhorto_archivo_encontrado.nombre_archivo,
        tamano=archivo_pdf_tamanio,
    )

    # Si pendientes_contador + 1 = total_contador
    if pendientes_contador + 1 >= total_contador:
        # Generar el folio_seguimiento como un UUID
        folio_seguimiento = str(uuid.uuid4())
        # Entonces ES EL ULTIMO ARCHIVO, se cambia el estado de exh_exhorto a RECIBIDO
        exh_exhorto_actualizado = update_set_exhorto(
            database=database,
            exh_exhorto=exh_exhorto,
            estado="RECIBIDO",
            folio_seguimiento=folio_seguimiento,
        )
        # Y se va a elaborar el acuse
        acuse = ExhExhortoArchivoFileDataAcuseOut(
            exhortoOrigenId=exh_exhorto_actualizado.exhorto_origen_id,
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
    return ExhExhortoArchivoFileOut(success=True, data=data)
