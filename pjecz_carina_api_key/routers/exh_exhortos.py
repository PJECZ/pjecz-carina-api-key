"""
Exh Exhortos, routers
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.safe_string import safe_clave, safe_email, safe_string, safe_telefono
from ..models.estados import Estado
from ..models.exh_exhortos import ExhExhorto
from ..models.exh_exhortos_archivos import ExhExhortoArchivo
from ..models.exh_exhortos_partes import ExhExhortoParte
from ..models.exh_exhortos_promoventes import ExhExhortoPromovente
from ..models.exh_externos import ExhExterno
from ..models.exh_tipos_diligencias import ExhTipoDiligencia
from ..models.municipios import Municipio
from ..models.permisos import Permiso
from ..schemas.exh_exhortos import (
    ExhExhortoConsultaOut,
    ExhExhortoIn,
    ExhExhortoOut,
    OneExhExhortoConsultaOut,
    OneExhExhortoOut,
)
from ..schemas.exh_exhortos_archivos import ExhExhortoArchivoItem
from ..schemas.exh_exhortos_partes import ExhExhortoParteItem
from ..settings import Settings, get_settings
from .autoridades import get_autoridad_with_clave_nd
from .exh_areas import get_exh_area_with_clave_nd
from .municipios import get_municipio_destino, get_municipio_origen

exh_exhortos = APIRouter(prefix="/api/v5/exh_exhortos")

TIPO_DILIGENCIA_CLAVE_POR_DEFECTO = "OTR"


def get_exhorto_with_exhorto_origen_id(database: Annotated[Session, Depends(get_db)], exhorto_origen_id: str) -> ExhExhorto:
    """Consultar un exhorto con su exhorto_origen_id"""

    # Validar exhorto_origen_id
    exhorto_origen_id = safe_string(exhorto_origen_id, max_len=64, do_unidecode=True, to_uppercase=False)
    if exhorto_origen_id == "":
        raise MyNotValidParamError("No es un 'exhorto origen id' válido")

    # Consultar el exhorto
    try:
        exh_exhorto = database.query(ExhExhorto).filter_by(exhorto_origen_id=exhorto_origen_id).filter_by(estatus="A").first()
    except (MultipleResultsFound, NoResultFound) as error:
        raise MyNotExistsError(f"No existe el exhorto con el 'exhorto origen id' {exhorto_origen_id}") from error

    # Entregar
    return exh_exhorto


def get_exhorto_with_folio_seguimiento(database: Annotated[Session, Depends(get_db)], folio_seguimiento: str) -> ExhExhorto:
    """Consultar un exhorto con su folio de seguimiento"""

    # Normalizar folio_seguimiento a 48 caracteres como máximo
    folio_seguimiento = safe_string(folio_seguimiento, max_len=64, do_unidecode=True, to_uppercase=False)
    if folio_seguimiento == "":
        raise MyNotValidParamError("No es un 'folio seguimiento' válido")

    # Consultar el exhorto
    exh_exhorto = database.query(ExhExhorto).filter_by(folio_seguimiento=folio_seguimiento).filter_by(estatus="A").first()
    if exh_exhorto is None:
        raise MyNotExistsError(f"No existe el exhorto con folio de seguimiento {folio_seguimiento}")

    # Entregar
    return exh_exhorto


@exh_exhortos.get("/folio_seguimiento/{folio_seguimiento}", response_model=OneExhExhortoConsultaOut)
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
        exh_exhorto = get_exhorto_with_folio_seguimiento(database, folio_seguimiento)
    except (MyNotExistsError, MyNotValidParamError) as error:
        return OneExhExhortoConsultaOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Inicializar listado de partes
    partes = []

    # Pasar las partes del exhorto a instancias de ExhExhortoParteIn
    for exh_exhorto_parte in exh_exhorto.exh_exhortos_partes:
        partes.append(
            ExhExhortoParteItem(
                nombre=exh_exhorto_parte.nombre,
                apellidoPaterno=exh_exhorto_parte.apellido_paterno,
                apellidoMaterno=exh_exhorto_parte.apellido_materno,
                genero=exh_exhorto_parte.genero,
                esPersonaMoral=exh_exhorto_parte.es_persona_moral,
                tipoParte=exh_exhorto_parte.tipo_parte,
                tipoParteNombre=exh_exhorto_parte.tipo_parte_nombre,
                correoElectronico=exh_exhorto_parte.correoElectronico,
                telefono=exh_exhorto_parte.telefono,
            )
        )

    # Inicializar listado de archivos
    archivos = []

    # Pasar los archivos del exhorto a instancias de ExhExhortoArchivoOut
    for exh_exhorto_archivo in exh_exhorto.exh_exhortos_archivos:
        archivos.append(
            ExhExhortoArchivoItem(
                nombreArchivo=exh_exhorto_archivo.nombre_archivo,
                hashSha1=exh_exhorto_archivo.hash_sha1,
                hashSha256=exh_exhorto_archivo.hash_sha256,
                tipoDocumento=exh_exhorto_archivo.tipo_documento,
            )
        )

    # Consultar el municipio de destino
    municipio_destino = database.query(Municipio).get(exh_exhorto.municipio_destino_id)

    # Consultar el estado de destino
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
    )

    # Entregar
    return OneExhExhortoConsultaOut(success=True, message="Consulta hecha con éxito", errors=[], data=data)


@exh_exhortos.post("/recibir", response_model=OneExhExhortoOut)
async def recibir_exhorto_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    exh_exhorto_in: ExhExhortoIn,
):
    """Recepción de datos de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Inicializar listado de errores
    errores = []

    # Validar exhortoOrigenId
    exhorto_origen_id = safe_string(exh_exhorto_in.exhortoOrigenId, max_len=64, do_unidecode=True, to_uppercase=False)
    if exhorto_origen_id == "":
        errores.append("No es válido exhortoOrigenId")

    # Consultar nuestro estado
    estado_destino = database.query(Estado).get(settings.estado_clave)
    if estado_destino is None:
        errores.append(f"No existe el estado de destino {settings.estado_clave}")

    # Validar municipioDestinoId, obligatorio y es un identificador INEGI
    try:
        municipio_destino = get_municipio_destino(database, settings, exh_exhorto_in.municipioDestinoId)
    except MyAnyError as error:
        errores.append(str(error))

    # Consultar nuestro estado en exh_externos
    estado_destino_exh_externo = database.query(ExhExterno).filter_by(estado_id=estado_destino.id).first()
    if estado_destino_exh_externo is None:
        errores.append(f"No existe el registro del estado {settings.estado_clave} en exh_externos")

    # Validar materiaClave, que la tenga nuestro estado
    materia_clave = ""
    materia_nombre = ""
    if estado_destino_exh_externo:
        materias = estado_destino_exh_externo.materias  # Listado de diccionarios {"clave": "...", "nombre": "..."}
        if materias:
            materia_clave = safe_clave(exh_exhorto_in.materiaClave)
            for item in materias:
                if item["clave"] == materia_clave:
                    materia_nombre = item["nombre"]
                    break
    if materia_clave == "":
        errores.append(f"No hay materias en el estado {settings.estado_clave} en exh_externos")
    if materia_nombre == "":
        errores.append(f"No tiene la materia '{materia_clave}' el estado {settings.estado_clave} en exh_externos")

    # Validar estadoOrigenId y municipioOrigenId, enteros obligatorios y son identificadores INEGI
    try:
        municipio_origen = get_municipio_origen(database, exh_exhorto_in.estadoOrigenId, exh_exhorto_in.municipioOrigenId)
    except MyAnyError as error:
        errores.append(str(error))

    # Validar juzgadoOrigenId, es opcional
    juzgado_origen_id = None
    if exh_exhorto_in.juzgadoOrigenId is not None:
        juzgado_origen_id = safe_string(exh_exhorto_in.juzgadoOrigenId, max_len=64)

    # Validar juzgadoOrigenNombre, obligatorio
    juzgado_origen_nombre = safe_string(exh_exhorto_in.juzgadoOrigenNombre, save_enie=True)

    # Validar numeroExpedienteOrigen, obligatorio
    numero_expediente_origen = safe_string(exh_exhorto_in.numeroExpedienteOrigen)

    # Validar numeroOficioOrigen, es opcional
    numero_oficio_origen = None
    if exh_exhorto_in.numeroOficioOrigen is not None:
        numero_oficio_origen = safe_string(exh_exhorto_in.numeroOficioOrigen)

    # Validar tipoJuicioAsuntoDelitos, obligatorio
    tipo_juicio_asunto_delitos = safe_string(exh_exhorto_in.tipoJuicioAsuntoDelitos, save_enie=True)

    # Validar juezExhortante, es opcional
    juez_exhortante = None
    if exh_exhorto_in.juezExhortante is not None:
        juez_exhortante = safe_string(exh_exhorto_in.juezExhortante, save_enie=True)

    # Validar fojas, obligatorio, el valor 0 significa "No Especificado"
    fojas = 0
    if exh_exhorto_in.fojas > 0:
        fojas = exh_exhorto_in.fojas

    # Validar diasResponder, obligatorio, el valor de 0 significa "No Especificado"
    dias_responder = 0
    if exh_exhorto_in.diasResponder > 0:
        dias_responder = exh_exhorto_in.diasResponder

    # Validar tipoDiligenciaId
    tipo_diligencia_id = safe_string(exh_exhorto_in.tipoDiligenciaId, max_len=32)
    tipo_diligenciacion_nombre = None
    if tipo_diligencia_id:
        # Consultar TipoDiligencia por su clave
        exh_tipo_diligencia = database.query(ExhTipoDiligencia).filter_by(clave=tipo_diligencia_id).first()
        if exh_tipo_diligencia is None:
            exh_tipo_diligencia = database.query(ExhTipoDiligencia).filter_by(clave=TIPO_DILIGENCIA_CLAVE_POR_DEFECTO).first()
        tipo_diligenciacion_nombre = exh_tipo_diligencia.descripcion
    elif exh_exhorto_in.tipoDiligenciacionNombre is not None:
        exh_tipo_diligencia = database.query(ExhTipoDiligencia).filter_by(clave=TIPO_DILIGENCIA_CLAVE_POR_DEFECTO).first()
        tipo_diligenciacion_nombre = safe_string(exh_exhorto_in.tipoDiligenciacionNombre, save_enie=True)

    # Validar fechaOrigen, es opcional
    fecha_origen = None
    if exh_exhorto_in.fechaOrigen:
        try:
            fecha_origen = datetime.strptime(exh_exhorto_in.fechaOrigen, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            errores.append("La fecha de origen no tiene el formato correcto")

    # Validar observaciones, es opcional
    observaciones = None
    if exh_exhorto_in.observaciones is not None:
        observaciones = safe_string(exh_exhorto_in.observaciones, save_enie=True, max_len=1000)

    # Validar las partes
    if exh_exhorto_in.partes:
        for parte in exh_exhorto_in.partes:
            if safe_string(parte.nombre, save_enie=True) == "":
                errores.append("El nombre de una parte no es válido")
            genero = safe_string(parte.genero, to_uppercase=True)
            if genero != "" and genero not in ExhExhortoParte.GENEROS:
                errores.append("El género de una parte no es válido")
            if parte.tipoParte not in [0, 1, 2]:
                errores.append("El tipo_parte de una parte no es válido")

    # Validar que vengan archivos
    if len(exh_exhorto_in.archivos) == 0:
        errores.append("Faltan los archivos")

    # Validar los archivos
    for archivo in exh_exhorto_in.archivos:
        if archivo.nombreArchivo.strip() == "":
            errores.append("El nombre de un archivo no es válido")
        if archivo.tipoDocumento not in [1, 2, 3]:
            errores.append("El tipoDocumento de un archivo no es válido")

    # Validar los promoventes
    if exh_exhorto_in.promoventes:
        for promovente in exh_exhorto_in.promoventes:
            if safe_string(promovente.nombre, save_enie=True) == "":
                errores.append("El nombre de un promovente no es válido")
            genero = safe_string(promovente.genero, to_uppercase=True)
            if genero != "" and genero not in ExhExhortoParte.GENEROS:
                errores.append("El género de un promovente no es válido")
            if promovente.tipoParte not in [0, 1, 2]:
                errores.append("El tipo_parte de un promovente no es válido")

    # Área de recepción, es NO DEFINIDO
    try:
        exh_area = get_exh_area_with_clave_nd(database)
    except MyNotExistsError:
        errores.append("Falló porque no existe el área por defecto")

    # Juzgado/Área al que se turna el Exhorto, es NO DEFINIDO
    try:
        autoridad = get_autoridad_with_clave_nd(database)
    except MyNotExistsError:
        errores.append("Falló porque no existe la autoridad por defecto")

    # Si hubo errores, se termina de forma fallida
    if len(errores) > 0:
        return OneExhExhortoOut(success=False, message="Falló la recepción del exhorto", errors=errores, data=None)

    # Insertar el exhorto
    exh_exhorto = ExhExhorto(
        autoridad_id=autoridad.id,
        exh_area_id=exh_area.id,
        exh_tipo_diligencia_id=exh_tipo_diligencia.id,
        municipio_origen=municipio_origen,
        exhorto_origen_id=exhorto_origen_id,
        municipio_destino_id=municipio_destino.id,
        materia_clave=materia_clave,
        materia_nombre=materia_nombre,
        juzgado_origen_id=juzgado_origen_id,
        juzgado_origen_nombre=juzgado_origen_nombre,
        numero_expediente_origen=numero_expediente_origen,
        numero_oficio_origen=numero_oficio_origen,
        tipo_juicio_asunto_delitos=tipo_juicio_asunto_delitos,
        juez_exhortante=juez_exhortante,
        fojas=fojas,
        dias_responder=dias_responder,
        tipo_diligencia_id=tipo_diligencia_id,
        tipo_diligenciacion_nombre=tipo_diligenciacion_nombre,
        fecha_origen=fecha_origen,
        observaciones=observaciones,
        remitente="EXTERNO",
        estado="PENDIENTE",
    )
    database.add(exh_exhorto)
    database.commit()
    database.refresh(exh_exhorto)

    # OPCIONAL Insertar las partes
    if exh_exhorto_in.partes:
        for parte in exh_exhorto_in.partes:
            genero = safe_string(parte.genero, to_uppercase=True)
            if genero not in ExhExhortoParte.GENEROS:
                genero = "-"  # En persona moral se usa guion
            try:
                correo_electronico = safe_email(parte.correoElectronico)
            except ValueError:
                correo_electronico = None
            telefono = safe_telefono(parte.telefono)
            if telefono == "":
                telefono = None
            exh_exhorto_parte = ExhExhortoParte(
                exh_exhorto_id=exh_exhorto.id,
                nombre=safe_string(parte.nombre, save_enie=True),
                apellido_paterno=safe_string(parte.apellidoPaterno, save_enie=True),
                apellido_materno=safe_string(parte.apellidoMaterno, save_enie=True),
                genero=genero,
                es_persona_moral=parte.esPersonaMoral,
                tipo_parte=parte.tipoParte,
                tipo_parte_nombre=safe_string(parte.tipoParteNombre, save_enie=True),
                correo_electronico=correo_electronico,
                telefono=telefono,
            )
            database.add(exh_exhorto_parte)

    # Insertar los archivos
    for archivo in exh_exhorto_in.archivos:
        exh_exhorto_archivo = ExhExhortoArchivo(
            exh_exhorto_id=exh_exhorto.id,
            nombre_archivo=archivo.nombreArchivo,
            hash_sha1=archivo.hashSha1,
            hash_sha256=archivo.hashSha256,
            tipo_documento=archivo.tipoDocumento,
            estado="PENDIENTE",
            tamano=0,
            fecha_hora_recepcion=datetime.now(),
        )
        database.add(exh_exhorto_archivo)

    # OPCIONAL Insertar los promoventes
    if exh_exhorto_in.promoventes:
        for promovente in exh_exhorto_in.promoventes:
            genero = safe_string(promovente.genero, to_uppercase=True)
            if genero not in ExhExhortoPromovente.GENEROS:
                genero = "-"
            try:
                correo_electronico = safe_email(promovente.correoElectronico)
            except ValueError:
                correo_electronico = None
            telefono = safe_telefono(promovente.telefono)
            if telefono == "":
                telefono = None
            exh_exhorto_promovente = ExhExhortoPromovente(
                exh_exhorto_id=exh_exhorto.id,
                nombre=safe_string(promovente.nombre, save_enie=True),
                apellido_paterno=safe_string(promovente.apellidoPaterno, save_enie=True),
                apellido_materno=safe_string(promovente.apellidoMaterno, save_enie=True),
                genero=genero,
                es_persona_moral=promovente.esPersonaMoral,
                tipo_parte=promovente.tipoParte,
                tipo_parte_nombre=safe_string(promovente.tipoParteNombre, save_enie=True),
                correo_electronico=correo_electronico,
                telefono=telefono,
            )
            database.add(exh_exhorto_promovente)

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto)

    # Entregar
    data = ExhExhortoOut(
        exhortoOrigenId=str(exh_exhorto.exhorto_origen_id),
        fechaHora=exh_exhorto.creado.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoOut(success=True, message="Exhorto recibido con éxito", errors=[], data=data)
