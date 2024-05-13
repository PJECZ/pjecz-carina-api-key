"""
Exh Exhortos Archivos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_exhortos_archivos, get_exh_exhorto_archivo
from .schemas import ExhExhortoArchivoOut, OneExhExhortoArchivoOut, ExhExhortoArchivoFileIn

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
    """Entregar un archivo"""
    if current_user.permissions.get("EXH EXHORTOS ARCHIVOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"message": archivo.filename}
