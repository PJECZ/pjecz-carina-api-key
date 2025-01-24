"""
Modulos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..dependencies.safe_string import safe_string
from ..models.modulos import Modulo
from ..models.permisos import Permiso

modulos = APIRouter(prefix="/v4/modulos", tags=["usuarios"])


def get_modulos(database: Session) -> Any:
    """Consultar los modulos activos"""
    return database.query(Modulo).filter_by(estatus="A").order_by(Modulo.nombre)


def get_modulo(database: Session, modulo_id: int) -> Modulo:
    """Consultar un modulo por su id"""
    modulo = database.query(Modulo).get(modulo_id)
    if modulo is None:
        raise MyNotExistsError("No existe ese modulo")
    if modulo.estatus != "A":
        raise MyIsDeletedError("No es activo ese modulo, está eliminado")
    return modulo


def get_modulo_with_nombre(database: Session, nombre: str) -> Modulo:
    """Consultar un modulo por su nombre"""
    nombre = safe_string(nombre)
    if nombre == "":
        raise MyNotValidParamError("El nombre no es válido")
    modulo = database.query(Modulo).filter_by(nombre=nombre).first()
    if modulo is None:
        raise MyNotExistsError("No existe ese modulo")
    if modulo.estatus != "A":
        raise MyIsDeletedError("No es activo ese modulo, está eliminado")
    return modulo


@modulos.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
