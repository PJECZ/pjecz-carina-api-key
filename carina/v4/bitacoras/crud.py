"""
Bitacoras v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.bitacoras.models import Bitacora
from ..modulos.crud import get_modulo, get_modulo_with_nombre
from ..usuarios.crud import get_usuario, get_usuario_with_email


def get_bitacoras(
    database: Session,
    modulo_id: int = None,
    modulo_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los bitacoras activos"""
    consulta = database.query(Bitacora)
    if modulo_id is not None:
        modulo = get_modulo(database, modulo_id)
        consulta = consulta.filter_by(modulo_id=modulo.id)
    elif modulo_nombre is not None:
        modulo = get_modulo_with_nombre(database, modulo_nombre)
        consulta = consulta.filter_by(modulo_id=modulo.id)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    elif usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return consulta.filter_by(estatus="A").order_by(Bitacora.id)


def get_bitacora(database: Session, bitacora_id: int) -> Bitacora:
    """Consultar un bitacora por su id"""
    bitacora = database.query(Bitacora).get(bitacora_id)
    if bitacora is None:
        raise MyNotExistsError("No existe ese bitacora")
    if bitacora.estatus != "A":
        raise MyIsDeletedError("No es activo ese bitacora, está eliminado")
    return bitacora
