"""
Usuarios v4, authentications
"""

import re
from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from hashids import Hashids
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN
from unidecode import unidecode

from ..models.usuarios import Usuario
from ..schemas.usuarios import UsuarioInDB
from .database import get_db
from .exceptions import MyAuthenticationError

API_KEY_REGEXP = r"^\w+\.\w+\.\w+$"
X_API_KEY = APIKeyHeader(name="X-Api-Key")


def get_user(
    usuario_id: int,
    database: Session = Depends(get_db),
) -> Optional[UsuarioInDB]:
    """Consultar un usuario por su id"""
    usuario = database.query(Usuario).get(usuario_id)
    if usuario:
        return UsuarioInDB(
            id=usuario.id,
            distrito_id=usuario.distrito_id,
            distrito_clave=usuario.distrito_clave,
            distrito_nombre=usuario.distrito_nombre,
            distrito_nombre_corto=usuario.distrito_nombre_corto,
            autoridad_id=usuario.autoridad_id,
            autoridad_clave=usuario.autoridad_clave,
            autoridad_descripcion=usuario.autoridad_descripcion,
            autoridad_descripcion_corta=usuario.autoridad_descripcion_corta,
            email=usuario.email,
            nombres=usuario.nombres,
            apellido_paterno=usuario.apellido_paterno,
            apellido_materno=usuario.apellido_materno,
            curp=usuario.curp,
            puesto=usuario.puesto,
            username=usuario.email,
            permissions=usuario.permissions,
            hashed_password=usuario.contrasena,
            disabled=usuario.estatus != "A",
            api_key=usuario.api_key,
            api_key_expiracion=usuario.api_key_expiracion,
        )
    return None


def authenticate_user(
    api_key: str,
    database: Session,
) -> UsuarioInDB:
    """Autentificar un usuario por su api_key"""

    # Validar con expresion regular
    api_key = unidecode(api_key)
    if re.match(API_KEY_REGEXP, api_key) is None:
        raise MyAuthenticationError("No paso la validacion por expresion regular")

    # Separar el id, el email y la cadena aleatoria del api_key
    api_key_id, api_key_email, _ = api_key.split(".")

    # Decodificar el ID
    usuario_id = Usuario.decode_id(api_key_id)
    if usuario_id is None:
        raise MyAuthenticationError("No se pudo descifrar el ID")

    # Consultar
    usuario = get_user(usuario_id, database)
    if usuario is None:
        raise MyAuthenticationError("No se encontro el usuario")

    # Validar el api_key
    if usuario.api_key != api_key:
        raise MyAuthenticationError("No es igual la api_key al dato en la base de datos")

    # Validar el email
    if api_key_email != Hashids(salt=usuario.email, min_length=8).encode(1):
        raise MyAuthenticationError("No coincide el correo electronico")

    # Validar el tiempo de expiracion
    if usuario.api_key_expiracion < datetime.now():
        raise MyAuthenticationError("No vigente porque ya expiro")

    # Validad que sea activo
    if usuario.disabled:
        raise MyAuthenticationError("No es activo este usuario porque fue eliminado")

    # Entregar
    return usuario


async def get_current_active_user(
    api_key: str = Depends(X_API_KEY),
    database: Session = Depends(get_db),
) -> UsuarioInDB:
    """Obtener el usuario activo actual"""

    # Try-except
    try:
        usuario = authenticate_user(api_key, database)
    except MyAuthenticationError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(error)) from error

    # Entregar
    return usuario
