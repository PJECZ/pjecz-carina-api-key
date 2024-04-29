"""
Exh Exhortos Partes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoParteOut(BaseModel):
    """Esquema para entregar partes"""

    id: int | None = None
    exh_exhorto_id: int | None = None
    exh_exhorto_exhorto_origen_id: str | None = None
    nombre: str | None = None
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    genero: str | None = None
    es_persona_moral: bool | None = None
    tipo_parte: int | None = None
    tipo_parte_nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoParteOut(ExhExhortoParteOut, OneBaseOut):
    """Esquema para entregar un parte"""
