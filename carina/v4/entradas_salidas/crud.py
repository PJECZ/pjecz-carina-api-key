"""
Entradas-Salidas v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.entradas_salidas.models import EntradaSalida
from ..usuarios.crud import get_usuario, get_usuario_with_email


def get_entradas_salidas(
    database: Session,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los entradas-salidas activos"""
    consulta = database.query(EntradaSalida)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    elif usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return consulta.filter_by(estatus="A").order_by(EntradaSalida.id)


def get_entrada_salida(database: Session, entrada_salida_id: int) -> EntradaSalida:
    """Consultar un entrada-salida por su id"""
    entrada_salida = database.query(EntradaSalida).get(entrada_salida_id)
    if entrada_salida is None:
        raise MyNotExistsError("No existe ese entrada-salida")
    if entrada_salida.estatus != "A":
        raise MyIsDeletedError("No es activo ese entrada-salida, está eliminado")
    return entrada_salida
