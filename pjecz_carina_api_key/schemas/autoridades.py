"""
Autoridades v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridades"""

    clave: str
    descripcion_corta: str
    distrito_id: int
    distrito_clave: str
    descripcion: str
    es_extinto: bool
    es_cemasc: bool
    es_defensoria: bool
    es_jurisdiccional: bool
    es_notaria: bool
    es_organo_especializado: bool
    model_config = ConfigDict(from_attributes=True)


class OneAutoridadOut(OneBaseOut):
    """Esquema para entregar un autoridad"""

    data: AutoridadOut | None = None
