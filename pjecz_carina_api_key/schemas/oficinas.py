"""
Oficinas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int
    clave: str
    model_config = ConfigDict(from_attributes=True)


class OneOficinaOut(OneBaseOut):
    """Esquema para entregar un oficina"""

    data: OficinaOut | None = None
