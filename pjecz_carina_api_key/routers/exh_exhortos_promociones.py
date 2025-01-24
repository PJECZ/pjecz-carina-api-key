"""
Exh Exhortos Promociones v4, rutas (paths)
"""

from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.safe_string import safe_string
from ..models.exh_exhortos import ExhExhorto
from ..models.exh_exhortos_promociones import ExhExhortoPromocion
from ..models.exh_exhortos_promociones_archivos import ExhExhortoPromocionArchivo
from ..models.exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromovente
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_promociones import ExhExhortoPromocionIn, ExhExhortoPromocionOut, OneExhExhortoPromocionOut
from .exh_exhortos import get_exh_exhorto, get_exh_exhorto_by_folio_seguimiento

exh_exhortos_promociones = APIRouter(prefix="/v4/exh_exhortos_promociones", tags=["exh exhortos promociones"])


def get_exh_exhortos_promociones(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar las promociones de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoPromocion)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoPromocion.id)
    )


def get_exh_exhorto_promocion(database: Session, exh_exhorto_promocion_id: int) -> ExhExhortoPromocion:
    """Consultar una promoción de un exhorto por su id"""
    exh_exhorto_promocion = database.query(ExhExhortoPromocion).get(exh_exhorto_promocion_id)
    if exh_exhorto_promocion is None:
        raise MyNotExistsError("No existe esa promoción de exhorto")
    if exh_exhorto_promocion.estatus != "A":
        raise MyIsDeletedError("No es activa esa promoción de exhorto, está eliminada")
    return exh_exhorto_promocion


def get_exh_exhorto_promocion_by_folio_origen_promocion(
    database: Session,
    folio_seguimiento: str,
    folio_origen_promocion: str,
):
    """Consultar una promoción de un exhorto por su folio de origen de promoción"""

    # Normalizar a 48 caracteres permitidos como máximo
    folio_seguimiento = safe_string(folio_seguimiento, max_len=48, do_unidecode=True, to_uppercase=False)
    if folio_seguimiento == "":
        raise MyNotValidParamError("No es un folio de seguimiento válido")

    # Normalizar a 48 caracteres permitidos como máximo
    folio_origen_promocion = safe_string(folio_origen_promocion, max_len=48, do_unidecode=True, to_uppercase=False)
    if folio_origen_promocion == "":
        raise MyNotValidParamError("No es un folio de origen de promoción válido")

    # Consultar la promoción
    exh_exhorto_promocion = (
        database.query(ExhExhortoPromocion)
        .join(ExhExhorto)
        .filter(ExhExhorto.folio_seguimiento == folio_seguimiento)
        .filter(ExhExhortoPromocion.folio_origen_promocion == folio_origen_promocion)
        .filter(ExhExhortoPromocion.estatus == "A")
        .first()
    )

    # Verificar que exista
    if exh_exhorto_promocion is None:
        raise MyNotExistsError("No existe esa promoción de exhorto")

    # Entregar
    return exh_exhorto_promocion


def create_exh_exhorto_promocion(database: Session, exh_exhorto_promocion_in: ExhExhortoPromocionIn) -> ExhExhortoPromocion:
    """Crear una promoción de un exhorto"""

    # Inicializar
    exh_exhorto_promocion = ExhExhortoPromocion()

    # Consultar el exhorto
    exh_exhorto = get_exh_exhorto_by_folio_seguimiento(database, exh_exhorto_promocion_in.folioSeguimiento)

    # Definir las propiedades
    exh_exhorto_promocion.exh_exhorto_id = exh_exhorto.id
    exh_exhorto_promocion.folio_origen_promocion = exh_exhorto_promocion_in.folioOrigenPromocion
    exh_exhorto_promocion.fojas = exh_exhorto_promocion_in.fojas
    try:
        exh_exhorto_promocion.fecha_recepcion = datetime.strptime(exh_exhorto_promocion_in.fechaOrigen, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise MyNotValidParamError("La fecha no tiene el formato correcto")
    exh_exhorto_promocion.observaciones = safe_string(exh_exhorto_promocion_in.observaciones, save_enie=True, max_len=1000)
    exh_exhorto_promocion.remitente = "EXTERNO"
    exh_exhorto_promocion.estado = "ENVIADO"

    # Insertar la promoción
    database.add(exh_exhorto_promocion)
    database.commit()
    database.refresh(exh_exhorto_promocion)

    # Insertar los promoventes
    for promovente in exh_exhorto_promocion_in.promoventes:
        exh_exhorto_promocion_promovente = ExhExhortoPromocionPromovente()
        exh_exhorto_promocion_promovente.exh_exhorto_promocion_id = exh_exhorto_promocion.id
        exh_exhorto_promocion_promovente.nombre = safe_string(promovente.nombre, save_enie=True)
        exh_exhorto_promocion_promovente.apellido_paterno = safe_string(promovente.apellidoPaterno, save_enie=True)
        exh_exhorto_promocion_promovente.apellido_materno = safe_string(promovente.apellidoMaterno, save_enie=True)
        if promovente.genero in ExhExhortoPromocionPromovente.GENEROS:
            exh_exhorto_promocion_promovente.genero = promovente.genero
        else:
            exh_exhorto_promocion_promovente.genero = "-"
        exh_exhorto_promocion_promovente.es_persona_moral = promovente.esPersonaMoral
        exh_exhorto_promocion_promovente.tipo_parte = promovente.tipoParte
        exh_exhorto_promocion_promovente.tipo_parte_nombre = safe_string(promovente.tipoParteNombre, save_enie=True)
        database.add(exh_exhorto_promocion_promovente)

    # Insertar los archivos
    for archivo in exh_exhorto_promocion_in.archivos:
        exh_exhorto_promocion_archivo = ExhExhortoPromocionArchivo()
        exh_exhorto_promocion_archivo.exh_exhorto_promocion_id = exh_exhorto_promocion.id
        exh_exhorto_promocion_archivo.nombre_archivo = archivo.nombreArchivo
        exh_exhorto_promocion_archivo.hash_sha1 = archivo.hashSha1
        exh_exhorto_promocion_archivo.hash_sha256 = archivo.hashSha256
        exh_exhorto_promocion_archivo.tipo_documento = archivo.tipoDocumento
        exh_exhorto_promocion_archivo.estado = "PENDIENTE"
        exh_exhorto_promocion_archivo.tamano = 0
        exh_exhorto_promocion_archivo.fecha_hora_recepcion = datetime.now()
        database.add(exh_exhorto_promocion_archivo)

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto_promocion)

    # Entregar
    return exh_exhorto_promocion


def update_exh_exhorto_promocion(
    database: Session,
    exh_exhorto_promocion: ExhExhortoPromocion,
    **kwargs,
) -> ExhExhortoPromocion:
    """Actualizar una promoción de un exhorto"""
    for key, value in kwargs.items():
        setattr(exh_exhorto_promocion, key, value)
    database.add(exh_exhorto_promocion)
    database.commit()
    database.refresh(exh_exhorto_promocion)
    return exh_exhorto_promocion


@exh_exhortos_promociones.post("", response_model=OneExhExhortoPromocionOut)
async def recibir_exhorto_promocion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_promocion_in: ExhExhortoPromocionIn,
):
    """Recibir una promoción de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_promocion = create_exh_exhorto_promocion(database, exh_exhorto_promocion_in)
    except MyAnyError as error:
        return OneExhExhortoPromocionOut(
            success=False,
            message="Error al recibir la promoción del exhorto",
            errors=[str(error)],
            data=None,
        )
    data = ExhExhortoPromocionOut(
        folioSeguimiento=exh_exhorto_promocion.exh_exhorto.folio_seguimiento,
        folioOrigenPromocion=exh_exhorto_promocion.folio_origen_promocion,
        fechaHora=exh_exhorto_promocion.creado.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoPromocionOut(success=True, message="Promoción recibida con éxito", errors=[], data=data)
