"""
Municipios v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class MunicipioOut(BaseModel):
    """Esquema para entregar municipios"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneMunicipioOut(MunicipioOut, OneBaseOut):
    """Esquema para entregar un municipio"""
