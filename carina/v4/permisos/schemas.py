"""
Permisos v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class PermisoOut(BaseModel):
    """Esquema para entregar permisos"""

    id: int | None = None
    rol_id: int | None = None
    rol_nombre: str | None = None
    modulo_id: int | None = None
    modulo_nombre: str | None = None
    nivel: int | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OnePermisoOut(PermisoOut, OneBaseOut):
    """Esquema para entregar un permiso"""
