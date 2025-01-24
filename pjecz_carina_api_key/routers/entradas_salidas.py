"""
Entradas-Salidas v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.entradas_salidas import EntradaSalida
from ..models.permisos import Permiso
from .usuarios import get_usuario, get_usuario_with_email

entradas_salidas = APIRouter(prefix="/v4/entradas_salidas", tags=["usuarios"])


def get_entradas_salidas(
    database: Session,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar las entradas-salidas activos"""
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


@entradas_salidas.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("ENTRADAS SALIDAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
