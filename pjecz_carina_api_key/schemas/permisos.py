"""
Permisos, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class PermisoOut(BaseModel):
    """Esquema para entregar permisos"""

    id: int
    rol_id: int
    rol_nombre: str
    modulo_id: int
    modulo_nombre: str
    nivel: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OnePermisoOut(OneBaseOut):
    """Esquema para entregar un permiso"""

    data: PermisoOut | None = None
