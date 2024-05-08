"""
Exh Areas v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhAreaOut(BaseModel):
    """Esquema para entregar areas"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhAreaOut(OneBaseOut):
    """Esquema para entregar un area"""

    data: ExhAreaOut | None = None
