"""
Exh Areas v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhAreaOut(BaseModel):
    """Esquema para entregar areas"""

    clave: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneExhAreaOut(OneBaseOut):
    """Esquema para entregar un area"""

    data: ExhAreaOut | None = None
