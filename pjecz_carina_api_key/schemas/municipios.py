"""
Municipios v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class MunicipioOut(BaseModel):
    """Esquema para entregar municipios"""

    clave: str
    nombre: str
    estado_clave: str
    estado_nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneMunicipioOut(OneBaseOut):
    """Esquema para entregar un municipio"""

    data: MunicipioOut | None = None
