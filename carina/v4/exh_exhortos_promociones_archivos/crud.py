"""
Exh Exhortos Promociones Archivos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_exhortos_promociones_archivos.models import ExhExhortoPromocionArchivo
from carina.v4.exh_exhortos_promociones.crud import get_exh_exhorto_promocion
from lib.exceptions import MyIsDeletedError, MyNotExistsError


def get_exh_exhortos_promociones_archivos(database: Session, exh_exhorto_promocion_id: int, estado: str = None) -> Any:
    """Consultar los archivos de una promoción de un exhorto"""
    exh_exhorto_promocion = get_exh_exhorto_promocion(database, exh_exhorto_promocion_id)
    consulta = database.query(ExhExhortoPromocionArchivo).filter_by(exh_exhorto_promocion_id=exh_exhorto_promocion.id)
    if estado is not None:
        consulta = consulta.filter_by(estado=estado)
    return consulta.filter_by(estatus="A").order_by(ExhExhortoPromocionArchivo.id)


def get_exh_exhorto_promocion_archivo(database: Session, exh_exhorto_promocion_archivo_id: int) -> ExhExhortoPromocionArchivo:
    """Consultar un archivo de una promoción de un exhorto por su id"""
    exh_exhorto_promocion_archivo = database.query(ExhExhortoPromocionArchivo).get(exh_exhorto_promocion_archivo_id)
    if exh_exhorto_promocion_archivo is None:
        raise MyNotExistsError("No existe ese archivo de promoción de exhorto")
    if exh_exhorto_promocion_archivo.estatus != "A":
        raise MyIsDeletedError("No es activo ese archivo de promoción de exhorto, está eliminado")
    return exh_exhorto_promocion_archivo


def update_exh_exhorto_promocion_archivo(
    database: Session, exh_exhorto_promocion_archivo: ExhExhortoPromocionArchivo, **kwargs
) -> ExhExhortoPromocionArchivo:
    """Actualizar un archivo de una promoción de un exhorto"""
    for key, value in kwargs.items():
        setattr(exh_exhorto_promocion_archivo, key, value)
    database.add(exh_exhorto_promocion_archivo)
    database.commit()
    database.refresh(exh_exhorto_promocion_archivo)
    return exh_exhorto_promocion_archivo
