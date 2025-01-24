"""
Usuarios v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..dependencies.safe_string import safe_email, safe_string
from ..models.permisos import Permiso
from ..models.usuarios import Usuario
from .autoridades import get_autoridad, get_autoridad_with_clave

usuarios = APIRouter(prefix="/v4/usuarios", tags=["usuarios"])


def get_usuarios(
    database: Session,
    apellido_paterno: str = None,
    apellido_materno: str = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    email: str = None,
    nombres: str = None,
) -> Any:
    """Consultar los usuarios activos"""
    consulta = database.query(Usuario)
    if apellido_paterno is not None:
        apellido_paterno = safe_string(apellido_paterno)
        if apellido_paterno != "":
            consulta = consulta.filter(Usuario.apellido_paterno.contains(apellido_paterno))
    if apellido_materno is not None:
        apellido_materno = safe_string(apellido_materno)
        if apellido_materno != "":
            consulta = consulta.filter(Usuario.apellido_materno.contains(apellido_materno))
    if autoridad_id is not None:
        autoridad = get_autoridad(database, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(database, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    if email is not None:
        try:
            email = safe_email(email, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("El email no es válido") from error
        consulta = consulta.filter(Usuario.email.contains(email))
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres != "":
            consulta = consulta.filter(Usuario.nombres.contains(nombres))
    return consulta.filter_by(estatus="A").order_by(Usuario.email)


def get_usuario(database: Session, usuario_id: int) -> Usuario:
    """Consultar un usuario por su id"""
    usuario = database.query(Usuario).get(usuario_id)
    if usuario is None:
        raise MyNotExistsError("No existe ese usuario")
    if usuario.estatus != "A":
        raise MyIsDeletedError("No es activo ese usuario, está eliminado")
    return usuario


def get_usuario_with_email(database: Session, usuario_email: str) -> Usuario:
    """Consultar un usuario por su email"""
    try:
        email = safe_email(usuario_email)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    usuario = database.query(Usuario).filter_by(email=email).first()
    if usuario is None:
        raise MyNotExistsError("No existe ese usuario")
    if usuario.estatus != "A":
        raise MyIsDeletedError("No es activo ese usuario, está eliminado")
    return usuario


@usuarios.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
