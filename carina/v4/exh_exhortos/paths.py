"""
Exh Exhortos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos.crud import create_exh_exhorto, get_exh_exhorto_by_folio_seguimiento, receive_response_exh_exhorto
from carina.v4.exh_exhortos.schemas import (
    ExhExhortoConsultaOut,
    ExhExhortoIn,
    ExhExhortoOut,
    ExhExhortoRespuestaIn,
    ExhExhortoRespuestaOut,
    OneExhExhortoConsultaOut,
    OneExhExhortoOut,
    OneExhExhortoRespuestaOut,
)
from carina.v4.exh_exhortos_archivos.schemas import ExhExhortoArchivo
from carina.v4.exh_exhortos_partes.schemas import ExhExhortoParte
from carina.v4.municipios.crud import get_municipio
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos = APIRouter(prefix="/v4/exh_exhortos", tags=["exh exhortos"])


@exh_exhortos.post("/responder", response_model=OneExhExhortoRespuestaOut)
async def recibir_exhorto_respuesta_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_recibir_respuesta: ExhExhortoRespuestaIn,
):
    """Recepción de respuesta de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto = receive_response_exh_exhorto(database, exh_exhorto_recibir_respuesta)
    except MyAnyError as error:
        return OneExhExhortoRespuestaOut(success=False, message="Error al recibir la respuesta", errors=[str(error)], data=None)
    data = ExhExhortoRespuestaOut(
        exhortoId=exh_exhorto.exhorto_origen_id,
        respuestaOrigenId=exh_exhorto.respuesta_origen_id,
        fechaHora=exh_exhorto.respuesta_fecha_hora_recepcion.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoRespuestaOut(success=True, message="Respuesta recibida con éxito", errors=[], data=data)


@exh_exhortos.get("/{folio_seguimiento}", response_model=OneExhExhortoConsultaOut)
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
        return OneExhExhortoConsultaOut(success=False, message="Error al consultar el exhorto", errors=[str(error)], data=None)

    # Copiar las partes del exhorto a instancias de ExhExhortoParteIn
    partes = []
    for exh_exhorto_parte in exh_exhorto.exh_exhortos_partes:
        partes.append(
            ExhExhortoParte(
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
            ExhExhortoArchivo(
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
    data = ExhExhortoConsultaOut(
        exhortoOrigenId=str(exh_exhorto.exhorto_origen_id),
        folioSeguimiento=str(exh_exhorto.folio_seguimiento),
        estadoDestinoId=estado_destino.clave,
        estadoDestinoNombre=estado_destino.nombre,
        municipioDestinoId=int(municipio_destino.clave),
        municipioDestinoNombre=municipio_destino.nombre,
        materiaClave=exh_exhorto.materia_clave,
        materiaNombre=exh_exhorto.materia_nombre,
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
        fechaOrigen=exh_exhorto.fecha_origen.strftime("%Y-%m-%d %H:%M:%S"),
        observaciones=exh_exhorto.observaciones,
        archivos=archivos,
        fechaHoraRecepcion=exh_exhorto.creado.strftime("%Y-%m-%d %H:%M:%S"),
        municipioTurnadoId=exh_exhorto.autoridad.municipio.clave,
        municipioTurnadoNombre=exh_exhorto.autoridad.municipio.nombre,
        areaTurnadoId=exh_exhorto.exh_area.clave,
        areaTurnadoNombre=exh_exhorto.exh_area.nombre,
        numeroExhorto=exh_exhorto.numero_exhorto,
        urlInfo="https://carina.justiciadigital.gob.mx/",
        respuestaOrigenId=exh_exhorto.respuesta_origen_id,
    )

    # Entregar
    return OneExhExhortoConsultaOut(success=True, message="Consulta hecha con éxito", errors=[], data=data)


@exh_exhortos.post("", response_model=OneExhExhortoOut)
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
        return OneExhExhortoOut(success=False, message="Error al recibir el exhorto", errors=[str(error)], data=None)
    data = ExhExhortoOut(
        exhortoOrigenId=str(exh_exhorto.exhorto_origen_id),
        fechaHora=exh_exhorto.creado.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoOut(success=True, message="Exhorto recibido con éxito", errors=[], data=data)
