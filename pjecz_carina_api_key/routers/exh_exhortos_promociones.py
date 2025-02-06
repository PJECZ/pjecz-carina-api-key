"""
Exh Exhortos Promociones
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.safe_string import safe_string
from ..models.exh_exhortos import ExhExhorto
from ..models.exh_exhortos_promociones import ExhExhortoPromocion
from ..models.exh_exhortos_promociones_archivos import ExhExhortoPromocionArchivo
from ..models.exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromovente
from ..models.permisos import Permiso
from ..schemas.exh_exhortos_promociones import ExhExhortoPromocionIn, ExhExhortoPromocionOut, OneExhExhortoPromocionOut
from .exh_exhortos import get_exhorto_with_folio_seguimiento

exh_exhortos_promociones = APIRouter(prefix="/api/v5/exh_exhortos_promociones")


def get_exhorto_promocion_with_folio_seguimiento(
    database: Annotated[Session, Depends(get_db)],
    folio_seguimiento: str,
    folio_origen_promocion: str,
) -> ExhExhortoPromocion:
    """Consultar una promoción con el folio de seguimiento del exhorto y el folio origen de la promoción"""

    # Normalizar folio_seguimiento a 48 caracteres como máximo
    folio_seguimiento = safe_string(folio_seguimiento, max_len=48, do_unidecode=True, to_uppercase=False)
    if folio_seguimiento == "":
        raise MyNotValidParamError("No es un folio de seguimiento de exhorto válido")

    # Normalizar folio_seguimiento a 48 caracteres como máximo
    folio_origen_promocion = safe_string(folio_origen_promocion, max_len=48, do_unidecode=True, to_uppercase=False)
    if folio_origen_promocion == "":
        raise MyNotValidParamError("No es un folio de origen de la promoción válido")

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


@exh_exhortos_promociones.post("", response_model=OneExhExhortoPromocionOut)
async def recibir_exhorto_promocion_request(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_promocion_in: ExhExhortoPromocionIn,
):
    """Recibir una promoción de un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Inicializar listado de errores
    errores = []

    # Consultar el exhorto
    try:
        exh_exhorto = get_exhorto_with_folio_seguimiento(database, exh_exhorto_promocion_in.folioSeguimiento)
    except MyAnyError as error:
        return OneExhExhortoPromocionOut(success=False, message=str(error), errors=[str(error)], data=None)

    # Validar la fecha
    try:
        fecha_origen = datetime.strptime(exh_exhorto_promocion_in.fechaOrigen, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        errores.append("La fecha no tiene el formato correcto")

    # Si hubo errores, se termina de forma fallida
    if len(errores) > 0:
        return OneExhExhortoPromocionOut(success=False, message="Falló la recepción del exhorto", errors=errores, data=None)

    # Insertar la promoción
    exh_exhorto_promocion = ExhExhortoPromocion(
        exh_exhorto_id=exh_exhorto.id,
        folio_origen_promocion=exh_exhorto_promocion_in.folioOrigenPromocion,
        fojas=exh_exhorto_promocion_in.fojas,
        fecha_origen=fecha_origen,
        observaciones=safe_string(exh_exhorto_promocion_in.observaciones, save_enie=True, max_len=1000),
        remitente="EXTERNO",
        estado="ENVIADO",
    )
    database.add(exh_exhorto_promocion)
    database.commit()
    database.refresh(exh_exhorto_promocion)

    # Insertar los promoventes
    for promovente in exh_exhorto_promocion_in.promoventes:
        exh_exhorto_promocion_promovente = ExhExhortoPromocionPromovente(
            exh_exhorto_promocion_id=exh_exhorto_promocion.id,
            nombre=safe_string(promovente.nombre, save_enie=True),
            apellido_paterno=safe_string(promovente.apellidoPaterno, save_enie=True),
            apellido_materno=safe_string(promovente.apellidoMaterno, save_enie=True),
            genero=promovente.genero if promovente.genero in ExhExhortoPromocionPromovente.GENEROS else "-",
            es_persona_moral=promovente.esPersonaMoral,
            tipo_parte=promovente.tipoParte,
            tipo_parte_nombre=safe_string(promovente.tipoParteNombre, save_enie=True),
        )
        database.add(exh_exhorto_promocion_promovente)

    # Insertar los archivos
    for archivo in exh_exhorto_promocion_in.archivos:
        exh_exhorto_promocion_archivo = ExhExhortoPromocionArchivo(
            exh_exhorto_promocion_id=exh_exhorto_promocion.id,
            nombre_archivo=archivo.nombreArchivo,
            hash_sha1=archivo.hashSha1,
            hash_sha256=archivo.hashSha256,
            tipo_documento=archivo.tipoDocumento,
            estado="PENDIENTE",
            tamano=0,
            fecha_hora_recepcion=datetime.now(),
        )
        database.add(exh_exhorto_promocion_archivo)

    # Terminar la transacción
    database.commit()
    database.refresh(exh_exhorto_promocion)

    # Entregar
    data = ExhExhortoPromocionOut(
        folioSeguimiento=exh_exhorto_promocion.exh_exhorto.folio_seguimiento,
        folioOrigenPromocion=exh_exhorto_promocion.folio_origen_promocion,
        fechaHora=exh_exhorto_promocion.creado.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return OneExhExhortoPromocionOut(success=True, message="Promoción recibida con éxito", errors=[], data=data)
