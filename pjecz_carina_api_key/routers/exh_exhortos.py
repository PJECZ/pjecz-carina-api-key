"""
Exh Exhortos v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.safe_string import safe_clave, safe_string
from ..models.autoridades import Autoridad
from ..models.estados import Estado
from ..models.exh_areas import ExhArea
from ..models.exh_exhortos import ExhExhorto
from ..models.exh_exhortos_videos import ExhExhortoVideo
from ..models.exh_externos import ExhExterno
from ..models.municipios import Municipio
from ..models.permisos import Permiso
from ..schemas.exh_exhortos import (
    ExhExhortoConsultaOut,
    ExhExhortoIn,
    ExhExhortoOut,
    ExhExhortoRespuestaIn,
    ExhExhortoRespuestaOut,
    OneExhExhortoConsultaOut,
    OneExhExhortoOut,
    OneExhExhortoRespuestaOut,
)
from ..schemas.exh_exhortos_archivos import ExhExhortoArchivo
from ..schemas.exh_exhortos_partes import ExhExhortoParte
from .municipios import get_municipio

exh_exhortos = APIRouter(prefix="/v4/exh_exhortos", tags=["exh exhortos"])


ESTADO_DESTINO_NOMBRE = "COAHUILA DE ZARAGOZA"
ESTADO_DESTINO_ID = 5


def get_exh_exhortos(database: Session) -> Any:
    """Consultar los exhortos"""
    return database.query(ExhExhorto).filter_by(estatus="A").order_by(ExhExhorto.id)


def get_exh_exhorto(database: Session, exh_exhorto_id: int) -> ExhExhorto:
    """Consultar un exhorto por su id"""
    exh_exhorto = database.query(ExhExhorto).get(exh_exhorto_id)
    if exh_exhorto is None:
        raise MyNotExistsError("No existe ese exhorto")
    if exh_exhorto.estatus != "A":
        raise MyIsDeletedError("No es activo ese exhorto, está eliminado")
    return exh_exhorto


def get_exh_exhorto_by_exhorto_origen_id(database: Session, exhorto_origen_id: str) -> ExhExhorto:
    """Consultar un exhorto por su exhorto_origen_id"""

    # Normalizar a 48 caracteres permitidos como máximo
    exhorto_origen_id = safe_string(exhorto_origen_id, max_len=48, do_unidecode=True, to_uppercase=False)
    if exhorto_origen_id == "":
        raise MyNotValidParamError("No es un identificador válido")

    # Consultar
    exh_exhorto = database.query(ExhExhorto).filter_by(exhorto_origen_id=exhorto_origen_id).filter_by(estatus="A").first()

    # Verificar que exista
    if exh_exhorto is None:
        raise MyNotExistsError("No existe ese exhorto")

    # Entregar
    return exh_exhorto


def get_exh_exhorto_by_folio_seguimiento(database: Session, folio_seguimiento: str) -> ExhExhorto:
    """Consultar un exhorto por su folio de seguimiento"""

    # Normalizar a 48 caracteres permitidos como máximo
    folio_seguimiento = safe_string(folio_seguimiento, max_len=48, do_unidecode=True, to_uppercase=False)
    if folio_seguimiento == "":
        raise MyNotValidParamError("No es un folio de seguimiento válido")

    # Consultar
    exh_exhorto = database.query(ExhExhorto).filter_by(folio_seguimiento=folio_seguimiento).filter_by(estatus="A").first()

    # Verificar que exista
    if exh_exhorto is None:
        raise MyNotExistsError("No existe ese exhorto")

    # Entregar
    return exh_exhorto


def create_exh_exhorto(database: Session, exh_exhorto_in: ExhExhortoIn) -> ExhExhorto:
    """Crear un exhorto"""

    # Inicializar la instancia ExhExhorto
    exh_exhorto = ExhExhorto()

    # Definir exhorto_origen_id
    exh_exhorto.exhorto_origen_id = exh_exhorto_in.exhortoOrigenId

    # Consultar nuestro estado
    estado_destino = database.query(Estado).get(ESTADO_DESTINO_ID)
    if estado_destino is None:
        raise MyNotExistsError(f"No existe el estado de destino {ESTADO_DESTINO_NOMBRE}")

    # Consultar y validar el municipio destino, que es Identificador INEGI
    municipio_destino_clave = str(exh_exhorto_in.municipioDestinoId).zfill(3)
    municipio_destino = (
        database.query(Municipio).filter_by(estado_id=ESTADO_DESTINO_ID).filter_by(clave=municipio_destino_clave).first()
    )
    if municipio_destino is None:
        raise MyNotExistsError(f"No existe el municipio {municipio_destino_clave} en {ESTADO_DESTINO_NOMBRE}")
    exh_exhorto.municipio_destino_id = municipio_destino.id

    # Consultar ExhExterno de nuestro estado
    estado_destino_exh_externo = database.query(ExhExterno).filter_by(estado_id=estado_destino.id).first()
    if estado_destino_exh_externo is None:
        raise MyNotExistsError(f"No existe el registro de {ESTADO_DESTINO_NOMBRE} en exh_externos")

    # Tomar las materias de nuestro estado
    materias = estado_destino_exh_externo.materias
    if materias is None:
        raise MyNotExistsError(f"No hay materias para {ESTADO_DESTINO_NOMBRE}")

    # Validar que materia la tenga nuestro estado
    materia_clave = safe_clave(exh_exhorto_in.materiaClave)
    materia = next((materia for materia in materias if materia["clave"] == materia_clave), None)
    if materia is None:
        raise MyNotExistsError(f"No tiene la materia {materia_clave} en {ESTADO_DESTINO_NOMBRE}")
    exh_exhorto.materia_clave = materia_clave
    exh_exhorto.materia_nombre = materia["nombre"]

    # Consultar y validar el estado de origen, se espera un identificador de INEGI de dos dígitos
    estado_clave = str(exh_exhorto_in.estadoOrigenId).zfill(2)
    estado = database.query(Estado).filter_by(clave=estado_clave).first()
    if estado is None:
        raise MyNotExistsError("No existe ese estado de origen")

    # Consultar y validar el municipio de origen, se espera un identificador de INEGI de tres dígitos
    municipio_clave = str(exh_exhorto_in.municipioOrigenId).zfill(3)
    municipio = database.query(Municipio).filter_by(estado_id=estado.id).filter_by(clave=municipio_clave).first()
    if municipio is None:
        raise MyNotExistsError("No existe ese municipio de origen")
    exh_exhorto.municipio_origen = municipio

    # Identificador propio del Juzgado/Área que envía el Exhorto
    exh_exhorto.juzgado_origen_id = exh_exhorto_in.juzgadoOrigenId

    # Nombre del Juzgado/Área que envía el Exhorto
    exh_exhorto.juzgado_origen_nombre = exh_exhorto_in.juzgadoOrigenNombre

    # El número de expediente (o carpeta procesal, carpeta...) que tiene el asunto en el Juzgado de Origen
    exh_exhorto.numero_expediente_origen = exh_exhorto_in.numeroExpedienteOrigen

    # El número del oficio con el que se envía el exhorto, el que corresponde al control interno del Juzgado de origen
    exh_exhorto.numero_oficio_origen = exh_exhorto_in.numeroOficioOrigen

    # Nombre del tipo de Juicio, o asunto, listado de los delitos (para materia Penal)
    # que corresponde al Expediente del cual el Juzgado envía el Exhorto
    exh_exhorto.tipo_juicio_asunto_delitos = exh_exhorto_in.tipoJuicioAsuntoDelitos

    # Nombre completo del Juez del Juzgado o titular del Área que envía el Exhorto
    exh_exhorto.juez_exhortante = exh_exhorto_in.juezExhortante

    # Número de fojas que contiene el exhorto. El valor 0 significa "No Especificado"
    exh_exhorto.fojas = exh_exhorto_in.fojas

    # Cantidad de dias a partir del día que se recibió en el Poder Judicial exhortado
    # que se tiene para responder el Exhorto. El valor de 0 significa "No Especificado"
    exh_exhorto.dias_responder = exh_exhorto_in.diasResponder

    # Nombre del tipo de diligenciación que le corresponde al exhorto enviado.
    # Este puede contener valores como "Oficio", "Petición de Parte"
    exh_exhorto.tipo_diligenciacion_nombre = exh_exhorto_in.tipoDiligenciacionNombre

    # Fecha y hora en que el Poder Judicial exhortante registró que se envió el exhorto en su hora local.
    # En caso de no enviar este dato, el Poder Judicial exhortado puede tomar su fecha hora local.
    # Validar que el string sea de la forma YYYY-MM-DD HH:mm:ss
    try:
        exh_exhorto.fecha_origen = datetime.strptime(exh_exhorto_in.fechaOrigen, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise MyNotValidParamError("La fecha de origen no tiene el formato correcto")

    # Texto simple que contenga información extra o relevante sobre el exhorto.
    exh_exhorto.observaciones = exh_exhorto_in.observaciones

    # GUID/UUID... que sea único. Va a ser generado cuando se vaya a regresar el acuse con el último archivo.
    exh_exhorto.folio_seguimiento = ""

    # Área de recepción, 1 = NO DEFINIDO
    exh_exhorto.exh_area = database.query(ExhArea).filter_by(clave="ND").first()

    # Juzgado/Área al que se turna el Exhorto, por defecto ND
    exh_exhorto.autoridad = database.query(Autoridad).filter_by(clave="ND").first()

    # Número de Exhorto con el que se radica en el Juzgado/Área que se turnó el exhorto, por defecto ''
    exh_exhorto.numero_exhorto = ""

    # Remitente es EXTERNO
    exh_exhorto.remitente = "EXTERNO"

    # Estado es RECIBIDO
    exh_exhorto.estado = "RECIBIDO"

    # Insertar el exhorto
    database.add(exh_exhorto)
    database.commit()
    database.refresh(exh_exhorto)

    # Insertar las partes
    for parte in exh_exhorto_in.partes:
        exh_exhorto_parte = ExhExhortoParte()
        exh_exhorto_parte.exh_exhorto = exh_exhorto
        exh_exhorto_parte.nombre = safe_string(parte.nombre, save_enie=True)
        exh_exhorto_parte.apellido_paterno = safe_string(parte.apellidoPaterno, save_enie=True)
        exh_exhorto_parte.apellido_materno = safe_string(parte.apellidoMaterno, save_enie=True)
        if parte.genero in ExhExhortoParte.GENEROS:
            exh_exhorto_parte.genero = parte.genero
        else:
            exh_exhorto_parte.genero = "-"
        exh_exhorto_parte.es_persona_moral = parte.esPersonaMoral
        exh_exhorto_parte.tipo_parte = parte.tipoParte
        exh_exhorto_parte.tipo_parte_nombre = safe_string(parte.tipoParteNombre, save_enie=True)
        database.add(exh_exhorto_parte)

    # Insertar los archivos
    for archivo in exh_exhorto_in.archivos:
        exh_exhorto_archivo = ExhExhortoArchivo()
        exh_exhorto_archivo.exh_exhorto = exh_exhorto
        exh_exhorto_archivo.nombre_archivo = archivo.nombreArchivo
        exh_exhorto_archivo.hash_sha1 = archivo.hashSha1
        exh_exhorto_archivo.hash_sha256 = archivo.hashSha256
        exh_exhorto_archivo.tipo_documento = archivo.tipoDocumento
        exh_exhorto_archivo.estado = "PENDIENTE"
        exh_exhorto_archivo.tamano = 0
        exh_exhorto_archivo.fecha_hora_recepcion = datetime.now()
        database.add(exh_exhorto_archivo)

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto)

    # Entregar
    return exh_exhorto


def receive_response_exh_exhorto(database: Session, exh_exhorto_respuesta: ExhExhortoRespuestaIn) -> ExhExhorto:
    """Recibir la respuesta de un exhorto"""

    # Tomar de la respuesta el exhorto_origen_id
    exhorto_origen_id = safe_string(exh_exhorto_respuesta.exhortoId)

    # Consultar el exhorto
    exh_exhorto = get_exh_exhorto_by_exhorto_origen_id(database=database, exhorto_origen_id=exhorto_origen_id)

    # Actualizar el exhorto con los datos de la respuesta
    exh_exhorto.respuesta_origen_id = exh_exhorto_respuesta.respuestaOrigenId
    exh_exhorto.respuesta_municipio_turnado_id = exh_exhorto_respuesta.municipioTurnadoId
    exh_exhorto.respuesta_area_turnado_id = exh_exhorto_respuesta.areaTurnadoId
    exh_exhorto.respuesta_area_turnado_nombre = exh_exhorto_respuesta.areaTurnadoNombre
    exh_exhorto.respuesta_numero_exhorto = exh_exhorto_respuesta.numeroExhorto
    exh_exhorto.respuesta_tipo_diligenciado = exh_exhorto_respuesta.tipoDiligenciado
    exh_exhorto.respuesta_fecha_hora_recepcion = datetime.now()
    exh_exhorto.respuesta_observaciones = safe_string(exh_exhorto_respuesta.observaciones, save_enie=True)

    # El estado del exhorto cambia a RESPONDIDO
    exh_exhorto.estado = "RESPONDIDO"
    database.add(exh_exhorto)
    database.commit()

    # Insertar los archivos
    for archivo in exh_exhorto_respuesta.archivos:
        exh_exhorto_archivo = ExhExhortoArchivo()
        exh_exhorto_archivo.exh_exhorto = exh_exhorto
        exh_exhorto_archivo.nombre_archivo = archivo.nombreArchivo
        exh_exhorto_archivo.hash_sha1 = archivo.hashSha1
        exh_exhorto_archivo.hash_sha256 = archivo.hashSha256
        exh_exhorto_archivo.tipo_documento = archivo.tipoDocumento
        exh_exhorto_archivo.estado = "PENDIENTE"
        exh_exhorto_archivo.tamano = 0
        exh_exhorto_archivo.fecha_hora_recepcion = datetime.now()
        exh_exhorto_archivo.es_respuesta = True  # Es un archivo que viene de una respuesta
        database.add(exh_exhorto_archivo)

    # Insertar los videos
    for video in exh_exhorto_respuesta.videos:
        exh_exhorto_video = ExhExhortoVideo()
        exh_exhorto_video.exh_exhorto = exh_exhorto
        exh_exhorto_video.titulo = safe_string(video.titulo, save_enie=True)
        exh_exhorto_video.descripcion = safe_string(video.descripcion, save_enie=True)
        exh_exhorto_video.fecha = video.fecha
        exh_exhorto_video.url_acceso = video.urlAcceso
        database.add(exh_exhorto_video)

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto)

    # Entregar el exhorto actualizado
    return exh_exhorto


def update_exh_exhorto(
    database: Session,
    exh_exhorto: ExhExhorto,
    **kwargs,
) -> ExhExhorto:
    """Actualizar un exhorto"""
    for key, value in kwargs.items():
        setattr(exh_exhorto, key, value)
    database.add(exh_exhorto)
    database.commit()
    database.refresh(exh_exhorto)
    return exh_exhorto


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
