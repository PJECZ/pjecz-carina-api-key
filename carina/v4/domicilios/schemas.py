"""
Domicilios v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class DomicilioOut(BaseModel):
    """Esquema para entregar domicilios"""

    id: int | None = None
    edificio: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneDomicilioOut(OneBaseOut):
    """Esquema para entregar un domicilio"""

    data: DomicilioOut | None = None
