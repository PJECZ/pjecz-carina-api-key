"""
Estados v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class EstadoOut(BaseModel):
    """Esquema para entregar estados"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneEstadoOut(OneBaseOut):
    """Esquema para entregar un estado"""

    data: EstadoOut | None = None
