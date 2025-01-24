"""
Municipios v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class MunicipioOut(BaseModel):
    """Esquema para entregar municipios"""

    clave: str | None = None
    nombre: str | None = None
    estado_clave: str | None = None
    estado_nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneMunicipioOut(OneBaseOut):
    """Esquema para entregar un municipio"""

    data: MunicipioOut | None = None
