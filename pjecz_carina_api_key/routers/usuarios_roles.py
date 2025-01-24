"""
Usuarios-Roles v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.permisos import Permiso
from ..models.usuarios_roles import UsuarioRol
from .roles import get_rol, get_rol_with_nombre
from .usuarios import get_usuario, get_usuario_with_email

usuarios_roles = APIRouter(prefix="/v4/usuarios_roles", tags=["usuarios"])


def get_usuarios_roles(
    database: Session,
    rol_id: int = None,
    rol_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los usuarios-roles activos"""
    consulta = database.query(UsuarioRol)
    if rol_id is not None:
        rol = get_rol(database, rol_id)
        consulta = consulta.filter_by(rol_id=rol.id)
    elif rol_nombre is not None:
        rol = get_rol_with_nombre(database, rol_nombre)
        consulta = consulta.filter_by(rol_id=rol.id)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    elif usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return consulta.filter_by(estatus="A").order_by(UsuarioRol.id)


def get_usuario_rol(database: Session, usuario_rol_id: int) -> UsuarioRol:
    """Consultar un usuario-rol por su id"""
    usuario_rol = database.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        raise MyNotExistsError("No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese usuario-rol, está eliminado")
    return usuario_rol


@usuarios_roles.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
