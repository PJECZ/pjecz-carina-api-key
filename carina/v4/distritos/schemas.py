"""
Distritos v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class DistritoListOut(BaseModel):
    """Esquema para entregar distritos como listado"""

    id: int | None = None
    clave: str | None = None
    nombre_corto: str | None = None
    model_config = ConfigDict(from_attributes=True)


class DistritoOut(DistritoListOut):
    """Esquema para entregar distritos"""

    nombre: str | None = None
    es_distrito: bool | None = None
    es_jurisdiccional: bool | None = None


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
