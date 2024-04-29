"""
Exh Exhortos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoOut(BaseModel):
    """Esquema para entregar plural"""

    id: int | None = None
    exhorto_origen_id: str | None = None
    municipio_destino_id: int | None = None
    materia_id: int | None = None
    materia_nombre: str | None = None
    estado_origen_id: int | None = None
    municipio_origen_id: int | None = None
    juzgado_origen_id: str | None = None
    juzgado_origen_nombre: str | None = None
    numero_expediente_origen: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoOut(ExhExhortoOut, OneBaseOut):
    """Esquema para entregar un singular"""
