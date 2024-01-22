"""
Usuarios v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_usuarios, get_usuario_with_email
from .schemas import UsuarioOut, OneUsuarioOut

usuarios = APIRouter(prefix="/v4/usuarios", tags=["usuarios"])


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def paginado_usuarios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_paterno: str = None,
    apellido_materno: str = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    email: str = None,
    nombres: str = None,
):
    """Paginado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios(
            database=database,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            email=email,
            nombres=nombres,
        )
    except MyAnyError as error:
        return CustomPage(success=False, errors=str(error))
    return paginate(resultados)


@usuarios.get("/{usuario_email}", response_model=OneUsuarioOut)
async def detalle_usuario(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    usuario_email: str,
):
    """Detalle de un usuario a partir de su e-mail"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario = get_usuario_with_email(database, usuario_email)
    except MyAnyError as error:
        return OneUsuarioOut(success=False, errors=str(error))
    return OneUsuarioOut.model_validate(usuario)
