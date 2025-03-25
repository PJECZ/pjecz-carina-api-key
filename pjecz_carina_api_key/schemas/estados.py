"""
Estados, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class EstadoOut(BaseModel):
    """Esquema para entregar estados"""

    clave: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneEstadoOut(OneBaseOut):
    """Esquema para entregar un estado"""

    data: EstadoOut | None = None
