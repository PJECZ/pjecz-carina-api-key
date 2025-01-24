"""
Bitácoras v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.bitacoras import Bitacora
from ..models.permisos import Permiso
from .modulos import get_modulo, get_modulo_with_nombre
from .usuarios import get_usuario, get_usuario_with_email

bitacoras = APIRouter(prefix="/v4/bitacoras", tags=["usuarios"])


def get_bitacoras(
    database: Session,
    modulo_id: int = None,
    modulo_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar las bitácoras"""
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
    """Consultar un bitácora por su id"""
    bitacora = database.query(Bitacora).get(bitacora_id)
    if bitacora is None:
        raise MyNotExistsError("No existe ese bitacora")
    if bitacora.estatus != "A":
        raise MyIsDeletedError("No es activo ese bitacora, está eliminado")
    return bitacora


@bitacoras.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("BITACORAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
