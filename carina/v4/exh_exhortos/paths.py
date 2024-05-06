"""
Exh Exhortos v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import create_exh_exhorto, get_exh_exhortos, get_exh_exhorto
from .schemas import (
    ExhExhortoConfirmacionDatosExhortoRecibidoOut,
    ExhExhortoIn,
    ExhExhortoOut,
    OneExhExhortoConfirmacionDatosExhortoRecibidoOut,
    OneExhExhortoOut,
)
from ..exh_exhortos_archivos.schemas import ExhExhortoArchivoOut
from ..exh_exhortos_partes.schemas import ExhExhortoParteIn

exh_exhortos = APIRouter(prefix="/v4/exh_exhortos", tags=["exhortos"])


@exh_exhortos.get("", response_model=CustomPage[ExhExhortoOut])
async def paginado_exh_exhortos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de exhortos"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_exh_exhortos(database)
    except MyAnyError as error:
        return CustomPage(success=False, errors=[str(error)])
    return paginate(resultados)


@exh_exhortos.get("/{exh_exhorto_id}", response_model=OneExhExhortoOut)
async def detalle_exh_exhorto(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_id: int,
):
    """Detalle de una exhorto a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    except MyAnyError as error:
        return OneExhExhortoOut(success=False, errors=[str(error)])

    # Copiar las partes del exhorto a instancias de ExhExhortoParteIn
    partes = []
    for exh_exhorto_parte in exh_exhorto.exh_exhortos_partes:
        partes.append(
            ExhExhortoParteIn(
                nombre=exh_exhorto_parte.nombre,
                apellidoPaterno=exh_exhorto_parte.apellido_paterno,
                apellidoMaterno=exh_exhorto_parte.apellido_materno,
                genero=exh_exhorto_parte.genero,
                esPersonaMoral=exh_exhorto_parte.es_persona_moral,
                tipoParte=exh_exhorto_parte.tipo_parte,
                tipoParteNombre=exh_exhorto_parte.tipo_parte_nombre,
            )
        )
    exh_exhorto.partes = partes

    # Copiar los archivos del exhorto a instancias de ExhExhortoArchivoOut
    archivos = []
    for exh_exhorto_archivo in exh_exhorto.exh_exhortos_archivos:
        archivos.append(
            ExhExhortoArchivoOut(
                nombreArchivo=exh_exhorto_archivo.nombre_archivo,
                hashSha1=exh_exhorto_archivo.hash_sha1,
                hashSha256=exh_exhorto_archivo.hash_sha256,
                tipoDocumento=exh_exhorto_archivo.tipo_documento,
            )
        )
    exh_exhorto.archivos = archivos

    # Entregar un exhorto
    return OneExhExhortoOut(success=True, data=exh_exhorto)


@exh_exhortos.post("", response_model=OneExhExhortoConfirmacionDatosExhortoRecibidoOut)
async def recepcion_exh_exhorto(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto: ExhExhortoIn,
):
    """Recepción de datos de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto = create_exh_exhorto(database, exh_exhorto)
    except MyAnyError as error:
        return OneExhExhortoConfirmacionDatosExhortoRecibidoOut(success=False, message=str(error))
    data = ExhExhortoConfirmacionDatosExhortoRecibidoOut(
        exhortoOrigenId=exh_exhorto.exhorto_origen_id,
        fechaHora=exh_exhorto.creado,
    )
    return OneExhExhortoConfirmacionDatosExhortoRecibidoOut(success=True, data=data)
