"""
Usuarios v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class UsuarioOut(BaseModel):
    """Esquema para entregar usuarios"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    autoridad_id: int | None = None
    autoridad_clave: str | None = None
    autoridad_descripcion: str | None = None
    autoridad_descripcion_corta: str | None = None
    email: str | None = None
    nombres: str | None = None
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    curp: str | None = None
    puesto: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioOut(OneBaseOut):
    """Esquema para entregar un usuario"""

    data: UsuarioOut | None = None


class UsuarioInDB(UsuarioOut):
    """Usuario en base de datos"""

    username: str
    permissions: dict
    hashed_password: str
    disabled: bool
    api_key: str
    api_key_expiracion: datetime
