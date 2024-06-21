"""
Exh Exhortos v4, CRUD (create, read, update, and delete)
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from carina.core.autoridades.models import Autoridad
from carina.core.exh_areas.models import ExhArea
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError

from ...core.estados.models import Estado
from ...core.exh_exhortos.models import ExhExhorto
from ...core.exh_exhortos_archivos.models import ExhExhortoArchivo
from ...core.exh_exhortos_partes.models import ExhExhortoParte
from ...core.materias.models import Materia
from ...core.municipios.models import Municipio
from ..exh_exhortos.schemas import ExhExhortoIn

ESTADO_DESTINO_NOMBRE = "COAHUILA DE ZARAGOZA"
ESTADO_DESTINO_ID = 5


def get_exh_exhortos(database: Session) -> Any:
    """Consultar los exhortos activos"""
    consulta = database.query(ExhExhorto)
    return consulta.filter_by(estatus="A").order_by(ExhExhorto.id)


def get_exh_exhorto_by_exhorto_origen_id(database: Session, exhorto_origen_id: str) -> ExhExhorto:
    """Consultar un exhorto por su exhorto_origen_id"""
    try:
        uuid.UUID(exhorto_origen_id)
    except ValueError as error:
        raise MyNotValidParamError("No es un UUID válido") from error
    exh_exhorto = database.query(ExhExhorto).filter_by(exhorto_origen_id=exhorto_origen_id).first()
    if exh_exhorto is None:
        raise MyNotExistsError("No existe ese exhorto")
    if exh_exhorto.estatus != "A":
        raise MyIsDeletedError("No es activo ese exhorto, está eliminado")
    return exh_exhorto


def get_exh_exhorto_by_folio_seguimiento(database: Session, folio_seguimiento: str) -> ExhExhorto:
    """Consultar un exhorto por su folio de seguimiento"""
    try:
        uuid.UUID(folio_seguimiento)
    except ValueError as error:
        raise MyNotValidParamError("No es un UUID válido") from error
    exh_exhorto = database.query(ExhExhorto).filter_by(folio_seguimiento=folio_seguimiento).first()
    if exh_exhorto is None:
        raise MyNotExistsError("No existe ese exhorto")
    if exh_exhorto.estatus != "A":
        raise MyIsDeletedError("No es activo ese exhorto, está eliminado")
    return exh_exhorto


def create_exh_exhorto(database: Session, exh_exhorto_in: ExhExhortoIn) -> ExhExhorto:
    """Crear un exhorto"""

    # Inicializar la instancia ExhExhorto
    exh_exhorto = ExhExhorto()

    # Definir exhorto_origen_id
    exh_exhorto.exhorto_origen_id = exh_exhorto_in.exhortoOrigenId

    # Consultar y validar el municipio destino, que es Identificador INEGI
    municipio_destino_clave = str(exh_exhorto_in.municipioDestinoId).zfill(3)
    municipio_destino = (
        database.query(Municipio).filter_by(estado_id=ESTADO_DESTINO_ID).filter_by(clave=municipio_destino_clave).first()
    )
    if municipio_destino is None:
        raise MyNotExistsError(f"No existe el municipio de destino {municipio_destino_clave} en {ESTADO_DESTINO_NOMBRE}")
    exh_exhorto.municipio_destino_id = municipio_destino.id

    # Consultar y validar la materia
    materia = database.query(Materia).filter_by(clave=exh_exhorto_in.materiaClave).first()
    if materia is None:
        raise MyNotExistsError("No existe esa materia")
    exh_exhorto.materia = materia

    # Consultar y validar el estado y municipio de origen, que son Identificadores INEGI
    estado_clave = str(exh_exhorto_in.estadoOrigenId).zfill(2)
    estado = database.query(Estado).filter_by(clave=estado_clave).first()
    if estado is None:
        raise MyNotExistsError("No existe ese estado de origen")
    municipio_clave = str(exh_exhorto_in.municipioOrigenId).zfill(3)
    municipio = database.query(Municipio).filter_by(estado_id=estado.id).filter_by(clave=municipio_clave).first()
    if municipio is None:
        raise MyNotExistsError("No existe ese municipio de origen")
    exh_exhorto.municipio_origen_id = municipio.id

    # Identificador propio del Juzgado/Área que envía el Exhorto
    exh_exhorto.juzgado_origen_id = exh_exhorto_in.juzgadoOrigenId

    # Nombre del Juzgado/Área que envía el Exhorto
    exh_exhorto.juzgado_origen_nombre = exh_exhorto_in.juzgadoOrigenNombre

    # El número de expediente (o carpeta procesal, carpeta...) que tiene el asunto en el Juzgado de Origen
    exh_exhorto.numero_expediente_origen = exh_exhorto_in.numeroExpedienteOrigen

    # El número del oficio con el que se envía el exhorto, el que corresponde al control interno del Juzgado de origen
    exh_exhorto.numero_oficio_origen = exh_exhorto_in.numeroOficioOrigen

    # Nombre del tipo de Juicio, o asunto, listado de los delitos (para materia Penal) que corresponde al Expediente del cual el Juzgado envía el Exhorto
    exh_exhorto.tipo_juicio_asunto_delitos = exh_exhorto_in.tipoJuicioAsuntoDelitos

    # Nombre completo del Juez del Juzgado o titular del Área que envía el Exhorto
    exh_exhorto.juez_exhortante = exh_exhorto_in.juezExhortante

    # Número de fojas que contiene el exhorto. El valor 0 significa "No Especificado"
    exh_exhorto.fojas = exh_exhorto_in.fojas

    # Cantidad de dias a partir del día que se recibió en el Poder Judicial exhortado que se tiene para responder el Exhorto. El valor de 0 significa "No Especificado"
    exh_exhorto.dias_responder = exh_exhorto_in.diasResponder

    # Nombre del tipo de diligenciación que le corresponde al exhorto enviado. Este puede contener valores como "Oficio", "Petición de Parte"
    exh_exhorto.tipo_diligenciacion_nombre = exh_exhorto_in.tipoDiligenciacionNombre

    # Fecha y hora en que el Poder Judicial exhortante registró que se envió el exhorto en su hora local. En caso de no enviar este dato, el Poder Judicial exhortado puede tomar su fecha hora local.
    exh_exhorto.fecha_origen = exh_exhorto_in.fechaOrigen

    # Texto simple que contenga información extra o relevante sobre el exhorto.
    exh_exhorto.observaciones = exh_exhorto_in.observaciones

    # GUID/UUID... que sea único
    random_uuid = uuid.uuid4()
    exh_exhorto.folio_seguimiento = str(random_uuid)

    # Área de recepción, 1 = NO DEFINIDO
    exh_exhorto.exh_area = database.query(ExhArea).filter_by(clave="ND").first()

    # Juzgado/Área al que se turna el Exhorto, por defecto ND
    exh_exhorto.autoridad = database.query(Autoridad).filter_by(clave="ND").first()

    # Número de Exhorto con el que se radica en el Juzgado/Área que se turnó el exhorto, por defecto ''
    exh_exhorto.numero_exhorto = ""

    # Remitente es EXTERNO
    exh_exhorto.remitente = "EXTERNO"

    # Estado es PENDIENTE
    exh_exhorto.estado = "PENDIENTE"

    # Iniciar la transaccion, agregar el exhorto
    database.add(exh_exhorto)

    # Insertar las partes
    for parte in exh_exhorto_in.partes:
        database.add(
            ExhExhortoParte(
                exh_exhorto=exh_exhorto,
                nombre=parte.nombre,
                apellido_paterno=parte.apellidoPaterno,
                apellido_materno=parte.apellidoMaterno,
                genero=parte.genero,
                es_persona_moral=parte.esPersonaMoral,
                tipo_parte=parte.tipoParte,
                tipo_parte_nombre=parte.tipoParteNombre,
            )
        )

    # Insertar los archivos
    for archivo in exh_exhorto_in.archivos:
        database.add(
            ExhExhortoArchivo(
                exh_exhorto=exh_exhorto,
                nombre_archivo=archivo.nombreArchivo,
                hash_sha1=archivo.hashSha1,
                hash_sha256=archivo.hashSha256,
                tipo_documento=archivo.tipoDocumento,
                estado="PENDIENTE",
                tamano=0,
                fecha_hora_recepcion=datetime.now(),
            )
        )

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto)

    # Entregar
    return exh_exhorto


def update_set_exhorto(database: Session, exh_exhorto: ExhExhorto, **kwargs) -> ExhExhorto:
    """Actualizar un exhorto"""
    for key, value in kwargs.items():
        setattr(exh_exhorto, key, value)
    database.add(exh_exhorto)
    database.commit()
    database.refresh(exh_exhorto)
    return exh_exhorto
