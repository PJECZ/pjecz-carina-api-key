"""
Exh Exhortos Archivos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from carina.core.exh_exhortos_archivos.models import ExhExhortoArchivo
from carina.v4.exh_exhortos.crud import get_exh_exhorto
from lib.exceptions import MyIsDeletedError, MyNotExistsError


def get_exh_exhortos_archivos(database: Session, exh_exhorto_id: int, estado: str = None, es_respuesta: bool = None) -> Any:
    """Consultar los archivos de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    consulta = database.query(ExhExhortoArchivo).filter_by(exh_exhorto_id=exh_exhorto.id)
    if estado is not None:
        consulta = consulta.filter_by(estado=estado)
    if es_respuesta is not None:
        consulta = consulta.filter_by(es_respuesta=es_respuesta)
    return consulta.filter_by(estatus="A").order_by(ExhExhortoArchivo.id)


def get_exh_exhorto_archivo(database: Session, exh_exhorto_archivo_id: int) -> ExhExhortoArchivo:
    """Consultar un archivo por su id"""
    exh_exhorto_archivo = database.query(ExhExhortoArchivo).get(exh_exhorto_archivo_id)
    if exh_exhorto_archivo is None:
        raise MyNotExistsError("No existe ese archivo")
    if exh_exhorto_archivo.estatus != "A":
        raise MyIsDeletedError("No es activo ese archivo, está eliminado")
    return exh_exhorto_archivo


def update_exh_exhorto_archivo(
    database: Session,
    exh_exhorto_archivo: ExhExhortoArchivo,
    **kwargs,
) -> ExhExhortoArchivo:
    """Actualizar un archivo"""
    for key, value in kwargs.items():
        setattr(exh_exhorto_archivo, key, value)
    database.add(exh_exhorto_archivo)
    database.commit()
    database.refresh(exh_exhorto_archivo)
    return exh_exhorto_archivo
