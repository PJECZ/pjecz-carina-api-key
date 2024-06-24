"""
Exh Exhortos v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from ...core.permisos.models import Permiso
from ..exh_exhortos_archivos.schemas import ExhExhortoArchivoOut
from ..exh_exhortos_partes.schemas import ExhExhortoParteIn
from ..municipios.crud import get_municipio
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import create_exh_exhorto, get_exh_exhorto_by_folio_seguimiento
from .schemas import (
    ExhExhortoConfirmacionDatosExhortoRecibidoOut,
    ExhExhortoIn,
    ExhExhortoOut,
    OneExhExhortoConfirmacionDatosExhortoRecibidoOut,
    OneExhExhortoOut,
)

exh_exhortos = APIRouter(prefix="/v4/exh_exhortos", tags=["exhortos"])


@exh_exhortos.get("/{folio_seguimiento}", response_model=OneExhExhortoOut)
async def consultar_exhorto_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    folio_seguimiento: str,
):
    """Detalle de un exhorto a partir de su folio de seguimiento"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Consultar el exhorto
    try:
        exh_exhorto = get_exh_exhorto_by_folio_seguimiento(database, folio_seguimiento)
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

    # Definir la clave INEGI del municipio de destino
    municipio_destino = get_municipio(database, exh_exhorto.municipio_destino_id)

    # Definir la clave INEGI del estado de destino
    estado_destino = municipio_destino.estado

    # Definir datos del exhorto a entregar
    ext_extorto_data = ExhExhortoOut(
        exhortoOrigenId=str(exh_exhorto.exhorto_origen_id),
        folioSeguimiento=str(exh_exhorto.folio_seguimiento),
        estadoDestinoId=estado_destino.clave,
        estadoDestinoNombre=estado_destino.nombre,
        municipioDestinoId=municipio_destino.clave,
        municipioDestinoNombre=municipio_destino.nombre,
        materiaClave=exh_exhorto.materia.clave,
        materiaNombre=exh_exhorto.materia.nombre,
        estadoOrigenId=exh_exhorto.municipio_origen.estado.clave,
        estadoOrigenNombre=exh_exhorto.municipio_origen.estado.nombre,
        municipioOrigenId=exh_exhorto.municipio_origen.clave,
        municipioOrigenNombre=exh_exhorto.municipio_origen.nombre,
        juzgadoOrigenId=exh_exhorto.juzgado_origen_id,
        juzgadoOrigenNombre=exh_exhorto.juzgado_origen_nombre,
        numeroExpedienteOrigen=exh_exhorto.numero_expediente_origen,
        numeroOficioOrigen=exh_exhorto.numero_oficio_origen,
        tipoJuicioAsuntoDelitos=exh_exhorto.tipo_juicio_asunto_delitos,
        juezExhortante=exh_exhorto.juez_exhortante,
        partes=partes,
        fojas=exh_exhorto.fojas,
        diasResponder=exh_exhorto.dias_responder,
        tipoDiligenciacionNombre=exh_exhorto.tipo_diligenciacion_nombre,
        fechaOrigen=exh_exhorto.fecha_origen,
        observaciones=exh_exhorto.observaciones,
        archivos=archivos,
        fechaHoraRecepcion=exh_exhorto.creado,
        municipioTurnadoId=exh_exhorto.autoridad.municipio.clave,
        municipioTurnadoNombre=exh_exhorto.autoridad.municipio.nombre,
        areaTurnadoId=exh_exhorto.exh_area.clave,
        areaTurnadoNombre=exh_exhorto.exh_area.nombre,
        numeroExhorto=exh_exhorto.numero_exhorto,
        urlInfo="https://carina.justiciadigital.gob.mx/",
    )

    # Entregar
    return OneExhExhortoOut(success=True, data=ext_extorto_data)


@exh_exhortos.post("", response_model=OneExhExhortoConfirmacionDatosExhortoRecibidoOut)
async def recibir_exhorto_request(
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
        return OneExhExhortoConfirmacionDatosExhortoRecibidoOut(
            success=False,
            message="Error al recibir un exhorto",
            errors=[str(error)],
        )
    data = ExhExhortoConfirmacionDatosExhortoRecibidoOut(
        exhortoOrigenId=str(exh_exhorto.exhorto_origen_id),
        fechaHora=exh_exhorto.creado,
    )
    return OneExhExhortoConfirmacionDatosExhortoRecibidoOut(success=True, data=data)
