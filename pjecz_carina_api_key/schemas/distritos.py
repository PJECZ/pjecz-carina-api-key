"""
Distritos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id: int | None = None
    clave: str | None = None
    nombre_corto: str | None = None
    nombre: str | None = None
    es_distrito: bool | None = None
    es_jurisdiccional: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class OneDistritoOut(OneBaseOut):
    """Esquema para entregar un distrito"""

    data: DistritoOut | None = None
