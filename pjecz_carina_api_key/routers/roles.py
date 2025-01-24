"""
Roles v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..dependencies.safe_string import safe_string
from ..models.permisos import Permiso
from ..models.roles import Rol

roles = APIRouter(prefix="/v4/roles", tags=["usuarios"])


def get_roles(database: Session) -> Any:
    """Consultar los roles activos"""
    return database.query(Rol).filter_by(estatus="A").order_by(Rol.nombre)


def get_rol(database: Session, rol_id: int) -> Rol:
    """Consultar un rol por su id"""
    rol = database.query(Rol).get(rol_id)
    if rol is None:
        raise MyNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese rol, está eliminado")
    return rol


def get_rol_with_nombre(database: Session, nombre: str) -> Rol:
    """Consultar un rol por su nombre"""
    nombre = safe_string(nombre)
    if nombre == "":
        raise MyNotValidParamError("El nombre no es válido")
    rol = database.query(Rol).filter_by(nombre=nombre).first()
    if rol is None:
        raise MyNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese rol, está eliminado")
    return rol


@roles.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
