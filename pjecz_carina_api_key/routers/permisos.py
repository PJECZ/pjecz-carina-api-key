"""
Permisos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.permisos import Permiso
from .modulos import get_modulo, get_modulo_with_nombre
from .roles import get_rol, get_rol_with_nombre

permisos = APIRouter(prefix="/v4/permisos", tags=["usuarios"])


def get_permisos(
    database: Session,
    modulo_id: int = None,
    modulo_nombre: str = None,
    rol_id: int = None,
    rol_nombre: str = None,
) -> Any:
    """Consultar los permisos activos"""
    consulta = database.query(Permiso)
    if modulo_id is not None:
        modulo = get_modulo(database, modulo_id)
        consulta = consulta.filter_by(modulo_id=modulo.id)
    elif modulo_nombre is not None:
        modulo = get_modulo_with_nombre(database, modulo_nombre)
        consulta = consulta.filter_by(modulo_id=modulo.id)
    if rol_id is not None:
        rol = get_rol(database, rol_id)
        consulta = consulta.filter_by(rol_id=rol.id)
    elif rol_nombre is not None:
        rol = get_rol_with_nombre(database, rol_nombre)
        consulta = consulta.filter_by(rol_id=rol.id)
    return consulta.filter_by(estatus="A").order_by(Permiso.id)


def get_permiso(database: Session, permiso_id: int) -> Permiso:
    """Consultar un permiso por su id"""
    permiso = database.query(Permiso).get(permiso_id)
    if permiso is None:
        raise MyNotExistsError("No existe ese permiso")
    if permiso.estatus != "A":
        raise MyIsDeletedError("No es activo ese permiso, está eliminado")
    return permiso


@permisos.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
