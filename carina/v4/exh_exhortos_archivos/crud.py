"""
Exh Exhortos Archivos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ..exh_exhortos.crud import get_exh_exhorto
from ...core.exh_exhortos_archivos.models import ExhExhortoArchivo


def get_exh_exhortos_archivos(
    database: Session,
    exh_exhorto_id: int = None,
) -> Any:
    """Consultar los archivos activos"""
    consulta = database.query(ExhExhortoArchivo)
    if exh_exhorto_id is not None:
        exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
        consulta = consulta.filter_by(exh_exhorto_id=exh_exhorto.id)
    return consulta.filter_by(estatus="A").order_by(ExhExhortoArchivo.id)


def get_exh_exhorto_archivo(database: Session, exh_exhorto_archivo_id: int) -> ExhExhortoArchivo:
    """Consultar un archivo por su id"""
    exh_exhorto_archivo = database.query(ExhExhortoArchivo).get(exh_exhorto_archivo_id)
    if exh_exhorto_archivo is None:
        raise MyNotExistsError("No existe ese archivo")
    if exh_exhorto_archivo.estatus != "A":
        raise MyIsDeletedError("No es activo ese archivo, está eliminado")
    return exh_exhorto_archivo
