"""
Exh Exhortos Archivos v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi_pagination.ext.sqlalchemy import paginate

from config.settings import get_settings
from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage
from lib.google_cloud_storage import get_blob_name_from_url, get_media_type_from_filename, get_file_from_gcs, upload_file_to_gcs

from ...core.permisos.models import Permiso
from ..exh_exhortos.crud import get_exh_exhorto
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_exhortos_archivos, get_exh_exhorto_archivo
from .schemas import (
    ExhExhortoArchivoFileDataAcuseOut,
    ExhExhortoArchivoFileDataArchivoOut,
    ExhExhortoArchivoFileDataOut,
    ExhExhortoArchivoFileOut,
    ExhExhortoArchivoOut,
    OneExhExhortoArchivoOut,
)

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

    # Consultar y validar el exhorto a partir del exhortoOrigenId
    try:
        exh_exhorto = get_exh_exhorto(database, exhortoOrigenId)
    except MyAnyError as error:
        return ExhExhortoArchivoFileOut(success=False, errors=[str(error)])

    # Consultar los archivos del exhorto
    exh_exhortos_archivos = get_exh_exhortos_archivos(database, exhortoOrigenId).all()

    # Buscar el archivo del exhorto a partir del nombre del archivo
    se_encontro = False
    for exh_exhorto_archivo in exh_exhortos_archivos:
        if exh_exhorto_archivo.nombre_archivo == archivo.filename:
            se_encontro = True
            break

    # Si NO se encontró el archivo, entonces entregar un error
    if not se_encontro:
        return ExhExhortoArchivoFileOut(success=False, errors=["No se encontró el archivo"])

    # Validar la integridad del archivo con los hashes

    # Almacenar el archivo en Google Storage
    settings = get_settings()
    upload_file_to_gcs(
        bucket_name=settings.cloud_storage_deposito,
        blob_name=f"exh_exhortos_archivos/YYYY/MM/DD/{archivo.filename}",
        content_type="application/pdf",
        data=archivo.file,
    )

    # Definir los datos del archivo para la respuesta
    archivo = ExhExhortoArchivoFileDataArchivoOut(
        nombreArchivo=archivo.filename,
        tamano=1024,
    )

    # Definir los datos del acuse para la respuesta
    acuse = ExhExhortoArchivoFileDataAcuseOut(
        exhortoOrigenId="",
        folioSeguimiento="",
        fechaHoraRecepcion=datetime.now(),
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
